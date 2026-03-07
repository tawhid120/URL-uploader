FROM python:3.12-slim

# Ensure Python output is sent straight to the container logs without buffering
# and prevent .pyc files from being written to the container filesystem.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install aria2 for torrent downloads, ffmpeg for media processing,
# tini for proper PID 1 signal handling, and curl for health checks.
RUN apt-get update && \
    apt-get install -y --no-install-recommends aria2 ffmpeg curl tini && \
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

# Cloud platforms (Render, Railway, Heroku, Koyeb, etc.) inject PORT at
# runtime.  Default to 8080 so the image works out-of-the-box locally too.
ENV PORT=8080
EXPOSE ${PORT}

# Health check for the FastAPI dashboard – uses the lightweight /health endpoint.
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD ["sh", "-c", "curl -sf http://localhost:${PORT}/health || exit 1"]

# Use tini as PID 1 so that SIGTERM from the orchestrator is properly forwarded
# to the Python process, ensuring graceful shutdown on every platform.
ENTRYPOINT ["tini", "--"]
CMD ["python", "-m", "bot"]
