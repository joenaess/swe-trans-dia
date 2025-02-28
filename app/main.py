from fastapi import FastAPI, UploadFile, File, HTTPException
import whisperx
import torch
import io
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
batch_size = 16  # Adjust as needed
compute_type = "float16"  # Or "int8" if low on GPU memory

hf_token = os.getenv("HUGGINGFACE_TOKEN")

if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN not found in .env file.")


model = whisperx.load_model(
    "KBLab/kb-whisper-large", device, compute_type=compute_type, download_root="/app/cache"
)
model_a, metadata = whisperx.load_align_model(
    language_code="sv",  # Assuming Swedish, adjust if needed
    device=device,
    model_name="KBLab/wav2vec2-large-voxrex-swedish",
    model_dir="/app/cache",
)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".mp3", ".ogg")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .wav, .mp3, and .ogg are supported.")

    try:
        audio_bytes = await file.read()
        audio = whisperx.load_audio(io.BytesIO(audio_bytes))
        result = model.transcribe(audio, batch_size=batch_size)
        aligned_result = whisperx.align(
            result["segments"], model_a, metadata, audio, device, return_char_alignments=False
        )
        return {"segments": aligned_result["segments"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)