import streamlit as st
import requests
from tempfile import NamedTemporaryFile
import os

st.title("Simple Audio Transcription App")

audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])

if audio_file is not None:
    if st.button("Start Transcription"):
        with st.spinner("Transcribing..."):
            with NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(audio_file.read())

                try:
                    with open(temp_file.name, "rb") as f:
                        files = {"file": f}
                        response = requests.post("http://localhost:8000/transcribe/", files=files)
                        response.raise_for_status()  # Raise an exception for bad status codes

                    result = response.json()
                    st.write("## Transcription Results")
                    st.write(result)

                except requests.exceptions.RequestException as e:
                    st.error(f"Transcription error: {e}")

                finally:
                    os.remove(temp_file.name)