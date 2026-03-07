import os

from dotenv import load_dotenv

load_dotenv()

# Telegram API credentials
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "url_uploader_bot")

# Optional log channel
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))

# Plan limits: (max_files_per_day, max_bandwidth_bytes_per_day)
PLAN_LIMITS = {
    "free": {"files": 10, "bandwidth": 2 * 1024**3},          # 10 files, 2 GB
    "basic": {"files": 50, "bandwidth": 10 * 1024**3},        # 50 files, 10 GB
    "standard": {"files": 100, "bandwidth": 30 * 1024**3},    # 100 files, 30 GB
    "pro": {"files": float("inf"), "bandwidth": float("inf")},  # Unlimited
}

# Download directory
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
