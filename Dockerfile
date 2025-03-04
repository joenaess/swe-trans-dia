FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu22.04

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y ffmpeg python3-pip  # Install pip

RUN pip install --no-cache-dir -r requirements.txt  # Install all requirements with pip

COPY models/ /app/models/
COPY app/ /app/
COPY .env /app/.env

RUN ruff check .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]