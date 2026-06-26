FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install curl for Docker health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download GPT-2 model files during build (no RAM limit).
# At runtime, from_pretrained() loads from local cache instead of
# downloading over HTTP, which avoids network buffer memory overhead.
RUN python -c "\
from huggingface_hub import snapshot_download; \
snapshot_download('gpt2')"

COPY . .

# Ensure start script is executable
RUN chmod +x start.sh

CMD ["./start.sh"]
