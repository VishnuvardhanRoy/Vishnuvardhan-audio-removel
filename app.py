import streamlit as st
import noisereduce as nr
import librosa
import soundfile as sf
import os
import tempfile

st.title("🎧 Audio Noise Remover")
st.write("Upload your noisy audio file below.")

uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "mpeg", "ogg", "m4a"])

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = tmp.name

        st.write("### Original Audio:")
        st.audio(uploaded_file)
        st.info("🔄 Processing... please wait...")

        data, rate = librosa.load(temp_path, sr=22050, mono=True)
        reduced = nr.reduce_noise(y=data, sr=rate, stationary=True)
        
        out_path = "cleaned.wav"
        sf.write(out_path, reduced, rate)

        st.success("✅ Noise removed!")
        st.write("### Cleaned Audio:")
        st.audio(out_path)

        with open(out_path, "rb") as f:
            st.download_button("⬇️ Download", f.read(), "cleaned.wav", "audio/wav")

        os.remove(temp_path)
        os.remove(out_path)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")



