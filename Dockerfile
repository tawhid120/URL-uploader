FROM python:3.12-slim

# Install aria2 for torrent downloads and ffmpeg for media processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends aria2 ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd -m -r -s /bin/bash botuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the downloads directory exists and is writable
RUN mkdir -p /app/downloads && chown -R botuser:botuser /app

USER botuser

# Cloud platforms inject PORT; default to 8080
ENV PORT=8080
EXPOSE ${PORT}

# Health check for the FastAPI dashboard
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -sf http://localhost:${PORT}/ || exit 1

CMD ["python", "-m", "bot"]
