FROM python:3.12-slim

# Install aria2 for torrent downloads and ffmpeg for media processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends aria2 ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud platforms inject PORT; default to 8080
ENV PORT=8080
EXPOSE ${PORT}

CMD ["python", "-m", "bot"]
