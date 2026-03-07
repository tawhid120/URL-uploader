<div align="center">

# 🚀 URL Uploader Bot

### An advanced, subscription-based Telegram bot for downloading and uploading content from 1500+ sites.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-orange?style=for-the-badge&logo=telegram&logoColor=white)](https://docs.pyrogram.org/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-supported-red?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Educational-blue?style=for-the-badge)](#license)

<br/>

**Deploy Instantly** &nbsp;→&nbsp;
[![Deploy to Heroku](https://img.shields.io/badge/Heroku-430098?style=flat-square&logo=heroku&logoColor=white)](#-heroku)
[![Deploy to Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white)](#-render)
[![Deploy to Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)](#-railway)
[![Deploy to Koyeb](https://img.shields.io/badge/Koyeb-121212?style=flat-square&logo=koyeb&logoColor=white)](#-koyeb)

<br/>

[Features](#-features) · [Quick Start](#-quick-start) · [Cloud Deployment](#-cloud-deployment) · [Commands](#-bot-commands) · [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Premium Plans](#-premium-plans)
- [Quick Start](#-quick-start)
- [Configuration](#%EF%B8%8F-configuration)
- [Docker Deployment](#-docker-deployment)
- [Cloud Deployment](#-cloud-deployment)
  - [Heroku](#-heroku)
  - [Render](#-render)
  - [Railway](#-railway)
  - [Koyeb](#-koyeb)
- [VPS Deployment](#-vps-deployment)
- [Project Structure](#-project-structure)
- [Bot Commands](#-bot-commands)
- [Running Tests](#-running-tests)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

<table>
<tr>
<td width="50%">

**🔗 Universal Downloading**
- YouTube, Instagram, TikTok, Twitter, and 1500+ sites via yt-dlp
- Exact video quality selection (1080p, 720p, 480p…)
- Audio extraction from any video
- Cookie-based auth for restricted / age-gated content

</td>
<td width="50%">

**📤 Smart Uploading**
- Up to 4 GB uploads via user session (Premium)
- Custom thumbnails & captions per user
- Auto-split oversized files with FFmpeg
- Progress tracking during upload

</td>
</tr>
<tr>
<td width="50%">

**💎 Subscription System**
- Four premium tiers with daily limits
- Daily file & bandwidth usage tracking via MongoDB
- Bulk mode — queue up to 200 links at once (Premium)

</td>
<td width="50%">

**🔧 Administration**
- `/broadcast`, `/ban`, `/unban` admin commands
- Force-subscribe middleware
- Log channel for monitoring downloads
- User management via MongoDB

</td>
</tr>
</table>

## 🛠 Tech Stack

| Technology | Purpose |
|:-----------|:--------|
| [Pyrogram](https://docs.pyrogram.org/) | Telegram MTProto API framework |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Universal video/audio downloader |
| [FFmpeg](https://ffmpeg.org/) | Media processing & file splitting |
| [MongoDB](https://www.mongodb.com/) + [Motor](https://motor.readthedocs.io/) | Async database for users & usage tracking |
| [aiohttp](https://docs.aiohttp.org/) | Async HTTP client |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable management |

## 💎 Premium Plans

| Feature | Free | Basic | Standard | Pro |
|:--------|:----:|:-----:|:--------:|:---:|
| Daily Files | 10 | 50 | 100 | ∞ |
| Daily Bandwidth | 2 GB | 10 GB | 30 GB | ∞ |
| Bulk Upload | ❌ | ✅ | ✅ | ✅ |
| 4 GB Uploads | ❌ | ✅ | ✅ | ✅ |

## 🚀 Quick Start

### Prerequisites

| Requirement | Details |
|:------------|:--------|
| **Python** | 3.10 or higher |
| **MongoDB** | Local instance or [MongoDB Atlas](https://www.mongodb.com/atlas) (free tier available) |
| **FFmpeg** | Installed and available in your `PATH` |
| **Bot Token** | Obtain from [@BotFather](https://t.me/BotFather) |
| **API Credentials** | Obtain from [my.telegram.org](https://my.telegram.org) |

### Installation

```bash
# Clone the repository
git clone https://github.com/tawhid120/URL-uploader.git
cd URL-uploader

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials (see Configuration section below)

# Run the bot
python -m bot
```

## ⚙️ Configuration

Copy `.env.example` to `.env` and fill in the values:

| Variable | Required | Default | Description |
|:---------|:--------:|:--------|:------------|
| `API_ID` | ✅ | — | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | — | Telegram API hash from [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | ✅ | — | Bot token from [@BotFather](https://t.me/BotFather) |
| `MONGO_URI` | ✅ | `mongodb://localhost:27017` | MongoDB connection string |
| `DB_NAME` | ❌ | `url_uploader_bot` | MongoDB database name |
| `SESSION_STR` | ❌ | — | Pyrogram user session string for 4 GB uploads |
| `LOG_CHANNEL` | ❌ | `0` | Telegram channel ID for download logging |
| `FSUB_CHANNEL` | ❌ | — | Force-subscribe channel (username without `@`, or channel ID) |
| `ADMIN_IDS` | ❌ | — | Comma-separated admin user IDs (e.g. `123456789,987654321`) |

<details>
<summary><b>Example <code>.env</code> file</b></summary>

```env
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

</details>

## 🐳 Docker Deployment

Docker Compose is the easiest way to deploy — it sets up both the bot **and** MongoDB automatically.

### 1. Clone & configure

```bash
git clone https://github.com/tawhid120/URL-uploader.git
cd URL-uploader
cp .env.example .env
nano .env   # fill in API_ID, API_HASH, BOT_TOKEN, etc.
```

### 2. Start everything

```bash
docker compose up -d --build
```

This launches two containers:
| Container | Description |
|:----------|:------------|
| `url-uploader-bot` | The Telegram bot + FastAPI dashboard |
| `url-uploader-mongo` | MongoDB 7 database |

### 3. Useful commands

```bash
# View live logs
docker compose logs -f bot

# Restart the bot after config changes
docker compose restart bot

# Stop everything
docker compose down

# Stop and remove stored data (MongoDB volume)
docker compose down -v
```

<details>
<summary><b>Run without Compose (standalone container)</b></summary>

If you already have a MongoDB instance, you can run just the bot:

```bash
docker build -t url-uploader .
docker run -d --name url-uploader-bot \
    -e API_ID=12345 \
    -e API_HASH=abcdef1234567890 \
    -e BOT_TOKEN=123456:ABC-DEF \
    -e MONGO_URI=mongodb://your-mongo-host:27017 \
    -p 8080:8080 \
    url-uploader
```

</details>

## ☁️ Cloud Deployment

> **Prerequisites for all cloud platforms:** You need a [MongoDB Atlas](https://www.mongodb.com/atlas) database (free tier available). Local MongoDB is not available on cloud platforms, so set `MONGO_URI` to your Atlas connection string (e.g. `mongodb+srv://user:pass@cluster.mongodb.net/url_uploader_bot`).

### <img src="https://cdn.simpleicons.org/heroku/430098" width="18"/> Heroku

Heroku uses the included `heroku.yml` and `app.json` to build and run the bot as a Docker container.

**One-Click Deploy:**

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/tawhid120/URL-uploader)

**Manual CLI Deploy:**

```bash
# Login and create the app
heroku login
heroku create your-app-name --stack container

# Set required environment variables
heroku config:set API_ID=12345
heroku config:set API_HASH=abcdef1234567890abcdef1234567890
heroku config:set BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
heroku config:set MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/url_uploader_bot

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

> **Note:** Heroku's free tier has been discontinued. The Eco plan ($5/month) provides 1000 dyno hours per month.

---

### <img src="https://cdn.simpleicons.org/render/46E3B7" width="18"/> Render

Render uses the included `render.yaml` blueprint for automatic configuration. It builds from the Dockerfile and includes a health check on `/health`.

**One-Click Deploy:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/tawhid120/URL-uploader)

**Manual Setup:**

1. Go to [render.com](https://render.com/) → **New** → **Web Service**
2. Connect your GitHub repository
3. Render auto-detects the `Dockerfile` — no build command needed
4. Add environment variables under **Environment**:
   | Variable | Value |
   |:---------|:------|
   | `API_ID` | Your Telegram API ID |
   | `API_HASH` | Your Telegram API Hash |
   | `BOT_TOKEN` | Your Bot Token |
   | `MONGO_URI` | Your MongoDB Atlas connection string |
5. Click **Create Web Service**

> **Tip:** Render's free tier spins down after 15 minutes of inactivity. Use the Starter plan ($7/month) for always-on deployment, or set up an external cron ping to keep the free instance alive.

---

### <img src="https://cdn.simpleicons.org/railway/0B0D0E" width="18"/> Railway

Railway uses the included `railway.toml` for build and deploy configuration. It builds from the Dockerfile with health checks and automatic restarts.

**One-Click Deploy:**

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template?referralCode=tawhid120)

**Manual Setup:**

1. Go to [railway.com](https://railway.com/) → **New Project** → **Deploy from GitHub repo**
2. Select your forked repository
3. Railway auto-detects the `Dockerfile` and `railway.toml`
4. Go to **Variables** and add:
   | Variable | Value |
   |:---------|:------|
   | `API_ID` | Your Telegram API ID |
   | `API_HASH` | Your Telegram API Hash |
   | `BOT_TOKEN` | Your Bot Token |
   | `MONGO_URI` | Your MongoDB Atlas connection string |
5. Deploy triggers automatically on push

**CLI Deploy (alternative):**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and initialize
railway login
railway init

# Link to your project and deploy
railway link
railway up
```

> **Tip:** Railway provides $5 of free credits per month. The Hobby plan ($5/month) includes 8 GB RAM and 8 vCPUs — more than enough for this bot.

---

### <img src="https://cdn.simpleicons.org/koyeb/121212" width="18"/> Koyeb

Koyeb provides serverless deployment with global edge infrastructure and automatic HTTPS.

**Manual Setup:**

1. Go to [app.koyeb.com](https://app.koyeb.com/) → **Create App** → **GitHub**
2. Connect your repository and select the branch
3. Set **Builder** to **Dockerfile**
4. Under **Environment variables**, add:
   | Variable | Value |
   |:---------|:------|
   | `API_ID` | Your Telegram API ID |
   | `API_HASH` | Your Telegram API Hash |
   | `BOT_TOKEN` | Your Bot Token |
   | `MONGO_URI` | Your MongoDB Atlas connection string |
5. Set the **Health check path** to `/health`
6. Click **Deploy**

**CLI Deploy (alternative):**

```bash
# Install Koyeb CLI
curl -fsSL https://raw.githubusercontent.com/koyeb/koyeb-cli/master/install.sh | sh

# Login
koyeb login

# Deploy from GitHub
koyeb app create url-uploader-bot \
  --docker "github.com/tawhid120/URL-uploader" \
  --docker-dockerfile Dockerfile \
  --env API_ID=12345 \
  --env API_HASH=abcdef1234567890 \
  --env BOT_TOKEN=123456:ABC-DEF \
  --env MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/url_uploader_bot \
  --port 8080:http \
  --route /:8080
```

> **Tip:** Koyeb's free tier includes one Eco instance with 512 MB RAM — suitable for running this bot 24/7.

---

### 📊 Platform Comparison

| Feature | Heroku | Render | Railway | Koyeb |
|:--------|:------:|:------:|:-------:|:-----:|
| **Free Tier** | ❌ (Eco $5/mo) | ✅ (spins down) | ✅ ($5 credit) | ✅ (Eco instance) |
| **Always On (Free)** | — | ❌ | ✅ | ✅ |
| **Docker Support** | ✅ | ✅ | ✅ | ✅ |
| **Auto Deploy on Push** | ✅ | ✅ | ✅ | ✅ |
| **Custom Domains** | ✅ | ✅ | ✅ | ✅ |
| **Health Checks** | ✅ | ✅ | ✅ | ✅ |
| **One-Click Deploy** | ✅ | ✅ | ✅ | ❌ |

> **Recommendation:** For beginners, **Render** or **Railway** offer the easiest setup experience. For production workloads, **Railway** or **Koyeb** provide the best value with always-on free tiers.

## 🌐 VPS Deployment

> **Recommended:** 1 vCPU / 1 GB RAM instance (DigitalOcean, Hetzner, Contabo, etc.)

### 1. Install system dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

### 2. Install & start MongoDB

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

> **Alternative:** Use [MongoDB Atlas](https://www.mongodb.com/atlas) (free tier) and set `MONGO_URI` accordingly.

### 3. Clone, configure & run

```bash
git clone https://github.com/tawhid120/URL-uploader.git
cd URL-uploader
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # fill in your credentials
python -m bot
```

### 4. Keep the bot running with systemd

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

<details>
<summary><b>View logs</b></summary>

```bash
sudo journalctl -u url-uploader -f
```

</details>

## 📁 Project Structure

```
URL-uploader/
├── bot/
│   ├── __init__.py
│   ├── __main__.py                  # Entry point
│   ├── client.py                    # Pyrogram bot + user session clients
│   ├── config.py                    # Configuration (env vars & plan limits)
│   ├── dashboard.py                 # Admin web dashboard (FastAPI)
│   ├── database/
│   │   ├── __init__.py
│   │   └── users.py                 # MongoDB user operations
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── callbacks.py             # Inline-button callback handler
│   │   ├── commands/                # User-facing commands
│   │   │   ├── start.py             #   /start
│   │   │   ├── help.py              #   /help
│   │   │   ├── settings.py          #   /settings
│   │   │   ├── myplan.py            #   /myplan
│   │   │   └── upgrade.py           #   /upgrade
│   │   ├── admin/                   # Admin-only commands
│   │   │   └── commands.py          #   /broadcast, /ban, /unban
│   │   └── upload/                  # Content handling
│   │       ├── url_handler.py       #   URL download & upload
│   │       ├── bulk.py              #   /bulk and /abort
│   │       ├── cookie.py            #   /cookie and /delcookie
│   │       └── thumbnail.py         #   Photo thumbnail + /delthumb
│   └── helpers/
│       ├── __init__.py
│       ├── fsub.py                  # Force-subscribe check
│       ├── keyboards.py             # Inline keyboard layouts
│       ├── utils.py                 # Utility functions
│       ├── cookie/                  # Cookie helpers
│       │   ├── detector.py          #   Smart cookie auto-detection
│       │   └── validator.py         #   yt-dlp cookie validation
│       ├── download/                # Download helpers
│       │   ├── downloader.py        #   yt-dlp download logic
│       │   ├── playlist.py          #   Playlist / gallery downloads
│       │   └── torrent.py           #   Torrent & magnet-link handler
│       └── media/                   # Media processing helpers
│           ├── split.py             #   FFmpeg auto-split for large files
│           ├── thumbnail.py         #   Auto-thumbnail generator
│           └── zipper.py            #   ZIP packaging for playlists
├── tests/                           # Test suite
├── .env.example                     # Sample environment config
├── .gitignore
├── requirements.txt
└── README.md
```

## 🤖 Bot Commands

### User Commands

| Command | Description |
|:--------|:------------|
| `/start` | Initialize the bot and register your account |
| `/help` | Show the user guide |
| `/settings` | Manage preferences (thumbnail, caption, cookies) |
| `/myplan` | View your current plan and daily usage statistics |
| `/upgrade` | Browse available premium plans |
| `/bulk` | Batch upload up to 200 links at once (Premium) |
| `/abort` | Stop an active bulk upload process |
| `/cookie` | Upload login cookies for restricted content |
| `/delcookie` | Delete your saved cookies |
| `/delthumb` | Remove your custom thumbnail |
| 📸 *Send a photo* | Set a custom thumbnail for uploads |
| 🔗 *Send a URL* | Download and upload content to Telegram |

### Admin Commands

| Command | Description |
|:--------|:------------|
| `/broadcast` | Send a message to all registered users |
| `/ban <user_id>` | Ban a user from using the bot |
| `/unban <user_id>` | Unban a previously banned user |

## 🧪 Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

Please make sure your code passes all existing tests before submitting.

## 📄 License

This project is provided as-is for educational purposes.

## 🙏 Acknowledgements

- [Pyrogram](https://docs.pyrogram.org/) — Telegram MTProto API framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — Universal video/audio downloader
- [FFmpeg](https://ffmpeg.org/) — Media processing toolkit
- [MongoDB](https://www.mongodb.com/) — NoSQL database
- [FastAPI](https://fastapi.tiangolo.com/) — Web framework for the admin dashboard

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ by [tawhid120](https://github.com/tawhid120)

</div>