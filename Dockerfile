FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu22.04

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y ffmpeg python3-pip git  # Install pip

#RUN pip install fastapi torch==2.3.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118

#RUN pip install git+https://github.com/m-bain/whisperx.git

RUN pip install --no-cache-dir -r requirements.txt  # Install all requirements with pip

COPY models/ /app/models/
COPY app/ /app/
COPY .env /app/.env

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]