import streamlit as st
import noisereduce as nr
import librosa
import soundfile as sf
import os
import numpy as np

st.title("🎧 Audio Noise Remover")
st.write("Upload your noisy audio file below. **WAV files work best!**")

uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])

if uploaded_file is not None:
    try:
        # Read WAV file directly
        import scipy.io.wavfile as wavfile
        
        # Save uploaded file
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write("### Original Audio:")
        st.audio(uploaded_file)
        
        # Load audio
        rate, data = wavfile.read("temp_audio.wav")
        
        # Convert to float
        if data.dtype != np.float32:
            data = data.astype(np.float32) / 32768.0
        
        st.info("🔄 Processing noise removal...")
        
        # Remove noise
        reduced = nr.reduce_noise(y=data, sr=rate, stationary=True, prop_decrease=1.0)
        
        # Save cleaned audio
        wavfile.write("cleaned.wav", rate, (reduced * 32768).astype(np.int16))
        
        st.success("✅ Noise removed successfully!")
        st.write("### Cleaned Audio:")
        st.audio("cleaned.wav")
        
        # Download button
        with open("cleaned.wav", "rb") as f:
            st.download_button(
                label="⬇️ Download Cleaned Audio",
                data=f.read(),
                file_name="cleaned_audio.wav",
                mime="audio/wav"
            )
        
        # Cleanup
        os.remove("temp_audio.wav")
        os.remove("cleaned.wav")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Please upload a WAV file for best results")




