from fastapi import FastAPI, UploadFile, File, HTTPException, Query
import whisperx
import torch
import io
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
batch_size = 16
compute_type = "float16"

hf_token = os.getenv("HUGGINGFACE_TOKEN")

if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN not found in .env file.")

model = whisperx.load_model(
    "KBLab/kb-whisper-large",
    device,
    compute_type=compute_type,
    download_root="/app/models",
    auth_token=hf_token,
)
model_a, metadata = whisperx.load_align_model(
    language_code="sv",
    model_name="KBLab/wav2vec2-large-voxrex-swedish",
    model_dir="/app/models",
    auth_token=hf_token,
)

diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device, model_dir="/app/models")

@app.post("/transcribe/")
async def transcribe(
    file: UploadFile = File(...),
    min_speakers: int = Query(None, description="Minimum number of speakers"),
    max_speakers: int = Query(None, description="Maximum number of speakers"),
):
    if not file.filename.endswith((".wav", ".mp3", ".ogg")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .wav, .mp3, and .ogg are supported.")

    try:
        audio_bytes = await file.read()
        audio = whisperx.load_audio(io.BytesIO(audio_bytes))
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
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)