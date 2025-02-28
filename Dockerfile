FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu22.04
WORKDIR /app

COPY app/requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y ffmpeg curl

# Install uv
RUN curl -fsSL https://raw.githubusercontent.com/astral-sh/uv/main/install.sh | sh

# Install python packages using uv
RUN /root/.local/bin/uv pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

RUN ruff check .  # Run ruff to check for linting errors

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]