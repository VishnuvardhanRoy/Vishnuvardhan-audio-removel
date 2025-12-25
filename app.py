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
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = tmp.name

        st.write("### Original Audio:")
        st.audio(uploaded_file)
        st.info("🔄 Processing... please wait...")

        # Load audio with sr=22050 (standard sample rate)
        try:
            data, rate = librosa.load(temp_path, sr=22050, mono=True)
        except Exception as load_err:
            st.error(f"Failed to load audio: {str(load_err)}")
            st.info("💡 Tip: Try uploading a WAV file instead")
            os.remove(temp_path)
            st.stop()

        # Reduce noise
        reduced = nr.reduce_noise(y=data, sr=rate, stationary=True)

        # Save output
        out_path = "cleaned_audio.wav"
        sf.write(out_path, reduced, rate)

        st.success("✅ Noise removed successfully!")
        st.write("### Cleaned Audio:")
        st.audio(out_path)

        with open(out_path, "rb") as f:
            st.download_button(
                "⬇️ Download Cleaned Audio",
                f.read(),
                "cleaned_audio.wav",
                "audio/wav"
            )

        # Cleanup
        os.remove(temp_path)
        os.remove(out_path)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Try uploading a different audio format (WAV preferred)")

