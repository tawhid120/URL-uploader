FROM python:3.12-slim

# Python আউটপুট সরাসরি লগ-এ পাঠানোর জন্য
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# বিল্ড ডিপেন্ডেন্সি এবং প্রয়োজনীয় টুলস ইন্সটল করা
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    aria2 \
    ffmpeg \
    curl \
    tini \
    gcc \
    python3-dev \
    libssl-dev \
    libffi-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# নন-রুট ইউজার তৈরি
RUN useradd -m -r -s /bin/bash botuser

WORKDIR /app

# requirements.txt কপি এবং ইন্সটল
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ডাউনলোড ডিরেক্টরি তৈরি এবং পারমিশন সেট করা
RUN mkdir -p /app/downloads && chown -R botuser:botuser /app

USER botuser

ENV PORT=8080
EXPOSE ${PORT}

# হেলথ চেক
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD ["sh", "-c", "curl -sf http://localhost:${PORT}/health || exit 1"]

ENTRYPOINT ["tini", "--"]
CMD ["python", "-m", "bot"]
