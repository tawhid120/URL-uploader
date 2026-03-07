# URL Uploader Bot 🚀

An advanced, subscription-based Telegram bot for downloading and uploading content from YouTube, Instagram, TikTok, Twitter, and 1500+ more sites — powered by [Pyrogram](https://docs.pyrogram.org/), [yt-dlp](https://github.com/yt-dlp/yt-dlp), [FFmpeg](https://ffmpeg.org/), and [MongoDB](https://www.mongodb.com/).

## ✨ Features

- 🔗 **Universal Downloader** — YouTube, Instagram, TikTok, Twitter, Drive, Mega, Mediafire & 1500+ sites via yt-dlp
- 🎬 Choose exact video quality (1080p, 720p, 480p…)
- 🎵 Extract audio from any video
- 🍪 Cookie-based auth for restricted / age-gated content
- 🖼 Custom thumbnails & captions per user
- 💎 Premium tiers (Free / Basic / Standard / Pro) with daily limits
- 📊 Daily file & bandwidth usage tracking via MongoDB
- 📦 Bulk mode — queue up to 200 links at once (Premium)
- 📤 4 GB uploads via user session (Premium)
- ✂️ Auto-split oversized files with FFmpeg
- 📢 Force-subscribe middleware
- 🔨 Admin tools — `/broadcast`, `/ban`, `/unban`

## 📁 Project Structure

```
URL-uploader/
├── bot/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── client.py             # Pyrogram bot + user session clients
│   ├── config.py             # Configuration (env vars)
│   ├── database/
│   │   ├── __init__.py
│   │   └── users.py          # MongoDB user operations
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py          # /start command
│   │   ├── help.py           # /help command
│   │   ├── settings.py       # /settings command
│   │   ├── myplan.py         # /myplan command
│   │   ├── upgrade.py        # /upgrade command
│   │   ├── bulk.py           # /bulk and /abort commands (asyncio.Queue)
│   │   ├── cookie.py         # /cookie and /delcookie commands
│   │   ├── thumbnail.py      # Photo thumbnail + /delthumb
│   │   ├── admin.py          # /broadcast, /ban, /unban (admin only)
│   │   ├── url_handler.py    # URL processing, download & upload
│   │   └── callbacks.py      # Inline-button callback handler
│   └── helpers/
│       ├── __init__.py
│       ├── downloader.py     # yt-dlp download logic
│       ├── keyboards.py      # Inline keyboard layouts
│       ├── fsub.py           # Force-subscribe check
│       ├── split.py          # FFmpeg auto-split for large files
│       └── utils.py          # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_downloader.py
│   ├── test_keyboards.py
│   └── test_utils.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠 Setup & Run

### Prerequisites

- Python 3.10+
- MongoDB (local or [MongoDB Atlas](https://www.mongodb.com/atlas))
- FFmpeg installed and in your PATH
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)

### Step-by-step

1. **Clone the repository**

   ```bash
   git clone https://github.com/tawhid120/URL-uploader.git
   cd URL-uploader
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   # venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and fill in your credentials:

   ```
   API_ID=12345
   API_HASH=abcdef1234567890abcdef1234567890
   BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
   MONGO_URI=mongodb://localhost:27017
   DB_NAME=url_uploader_bot
   LOG_CHANNEL=0

   # Optional — for 4 GB uploads via user session
   SESSION_STR=

   # Optional — force-subscribe channel (username without @)
   FSUB_CHANNEL=

   # Admin user IDs (comma-separated)
   ADMIN_IDS=123456789
   ```

4. **Run the bot**

   ```bash
   python -m bot
   ```

## 🚀 VPS Deployment Guide

### 1. Provision a VPS

Use any provider (e.g. DigitalOcean, Hetzner, Contabo). A 1 vCPU / 1 GB RAM instance is sufficient for light usage.

### 2. Install system dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

### 3. Install & start MongoDB

```bash
sudo apt install -y gnupg curl
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
  https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update && sudo apt install -y mongodb-org
sudo systemctl enable --now mongod
```

Or use **MongoDB Atlas** (free tier) and set `MONGO_URI` accordingly.

### 4. Clone, configure & run

```bash
git clone https://github.com/tawhid120/URL-uploader.git
cd URL-uploader
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # fill in your credentials
python -m bot
```

### 5. Keep the bot running with systemd

Create `/etc/systemd/system/url-uploader.service`:

```ini
[Unit]
Description=URL Uploader Telegram Bot
After=network.target mongod.service

[Service]
User=your_username
WorkingDirectory=/home/your_username/URL-uploader
ExecStart=/home/your_username/URL-uploader/venv/bin/python -m bot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now url-uploader
sudo systemctl status url-uploader
```

View logs with:

```bash
sudo journalctl -u url-uploader -f
```

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Initialize the bot |
| `/help` | Show the user guide |
| `/settings` | Manage preferences (thumbnail, caption, cookies) |
| `/myplan` | View usage statistics |
| `/upgrade` | Browse premium plans |
| `/bulk` | Batch upload up to 200 links (premium) |
| `/abort` | Stop an active bulk process |
| `/cookie` | Manage login cookies |
| `/delcookie` | Delete saved cookies |
| `/delthumb` | Remove custom thumbnail |
| 📸 Send a photo | Set custom thumbnail |
| 🔗 Send a URL | Download & upload content |
| `/broadcast` | Send a message to all users (admin) |
| `/ban <user_id>` | Ban a user (admin) |
| `/unban <user_id>` | Unban a user (admin) |

## 📄 License

This project is provided as-is for educational purposes.