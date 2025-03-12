import os
import tempfile

import torch
import whisperx
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Query, UploadFile

load_dotenv()

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
batch_size = 16
compute_type = "float16"

hf_token = os.getenv("HUGGINGFACE_TOKEN")

if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN not found in .env file.")

model = whisperx.load_model(
    "KBLab/kb-whisper-small",  # change to large in prod
    device,
    compute_type=compute_type,
    download_root="/app/models",
)
model_a, metadata = whisperx.load_align_model(
    device=device,
    language_code="sv",
    model_name="KBLab/wav2vec2-large-voxrex-swedish",
    model_dir="/app/models",
)

diarize_model = whisperx.DiarizationPipeline(
    model_name="pyannote/speaker-diarization-3.1", use_auth_token=hf_token, device=device
)


@app.post("/transcribe/")
async def transcribe(
    file: UploadFile = File(...),
    min_speakers: int = Query(None, description="Minimum number of speakers"),
    max_speakers: int = Query(None, description="Maximum number of speakers"),
):
    if not file.filename.endswith((".wav", ".mp3", ".ogg")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .wav, .mp3, and .ogg are supported.")

    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio_path = temp_audio.name
            # Write the uploaded audio to the temporary file
            audio_bytes = await file.read()
            temp_audio.write(audio_bytes)

        # Load audio from the temporary file
        audio = whisperx.load_audio(temp_audio_path)
        result = model.transcribe(audio, batch_size=batch_size)
        aligned_result = whisperx.align(
            result["segments"], model_a, metadata, audio, device, return_char_alignments=False
        )

        if min_speakers is not None and max_speakers is not None:
            diarize_segments = diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)
        else:
            diarize_segments = diarize_model(audio)

        result = whisperx.assign_word_speakers(diarize_segments, aligned_result)

        return {"segments": result["segments"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
