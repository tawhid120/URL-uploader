# URL Uploader Bot 🚀

An advanced Telegram bot for downloading and uploading content from YouTube, Instagram, TikTok, Twitter, and many more sites — powered by [Pyrogram](https://docs.pyrogram.org/), [yt-dlp](https://github.com/yt-dlp/yt-dlp), and [MongoDB](https://www.mongodb.com/).

## ✨ Features

- 🔗 Download from YouTube, Instagram, TikTok, Twitter & more
- 🎬 Choose exact video quality (1080p, 720p, 480p…)
- 🎵 Extract audio from any video
- 🍪 Cookie-based auth for restricted content
- 🖼 Custom thumbnails per user
- 💎 Premium tiers (Free / Basic / Standard / Pro)
- 📊 Daily file & bandwidth usage tracking via MongoDB

## 📁 Project Structure

```
URL-uploader/
├── bot/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── client.py             # Pyrogram client setup
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
│   │   ├── bulk.py           # /bulk and /abort commands
│   │   ├── cookie.py         # /cookie and /delcookie commands
│   │   ├── thumbnail.py      # Photo thumbnail + /delthumb
│   │   ├── url_handler.py    # URL processing & download
│   │   └── callbacks.py      # Inline-button callback handler
│   └── helpers/
│       ├── __init__.py
│       ├── downloader.py     # yt-dlp download logic
│       ├── keyboards.py      # Inline keyboard layouts
│       └── utils.py          # Utility functions
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
   ```

4. **Run the bot**

   ```bash
   python -m bot
   ```

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Initialize the bot |
| `/help` | Show the user guide |
| `/settings` | Manage preferences |
| `/myplan` | View usage statistics |
| `/upgrade` | Browse premium plans |
| `/bulk` | Batch upload (premium) |
| `/abort` | Stop an active process |
| `/cookie` | Manage login cookies |
| `/delcookie` | Delete saved cookies |
| `/delthumb` | Remove custom thumbnail |
| 📸 Send a photo | Set custom thumbnail |
| 🔗 Send a URL | Download & upload content |

## 📄 License

This project is provided as-is for educational purposes.