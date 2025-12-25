import streamlit as st
import noisereduce as nr
import librosa
import soundfile as sf
import numpy as np
import os

st.title("🎧 Audio Noise Remover")
st.write("Upload your noisy audio file below.")
s
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "mpeg", "ogg"])

if uploaded_file is not None:

    
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("### Original Audio:")
    st.audio(temp_filename)
    st.info("Processing... this might take 10-20 seconds...")

    try:
        data, rate = librosa.load(temp_filename, sr=None)

     
        reduced_noise = nr.reduce_noise(y=data, sr=rate, stationary=True)

       
        output_filename = "clean_audio.wav"
        sf.write(output_filename, reduced_noise, rate)

        st.success("Success! Noise removed.")

        st.write("### 🔉 Cleaned Audio:")
        st.audio(output_filename, format="audio/wav")

        with open(output_filename, "rb") as file:
            st.download_button(
                label="⬇️ Download Clean Audio",
                data=file,
                file_name="clean_audio.wav",
                mime="audio/wav"
            )
        os.remove(temp_filename)

    except Exception as e:
        st.error(f"Error: {e}")

