import whisperx
import torch
import os
from dotenv import load_dotenv

load_dotenv()

device = "cpu"
compute_type = "float32"

hf_token = os.getenv("HUGGINGFACE_TOKEN")

if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN not found in .env file.")

model = whisperx.load_model(
    "KBLab/kb-whisper-large",
    device,
    compute_type=compute_type,
    download_root="models",
)

whisperx.load_align_model(
    language_code="sv",
    model_name="KBLab/wav2vec2-large-voxrex-swedish",
    model_dir="models",
    device=device,
)

diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device)

print("Models downloaded successfully!")