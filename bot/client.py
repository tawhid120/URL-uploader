from pyrogram import Client

from bot.config import API_ID, API_HASH, BOT_TOKEN, SESSION_STR

bot = Client(
    name="url_uploader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Optional user session for 4 GB uploads
user_session: Client | None = None
if SESSION_STR:
    user_session = Client(
        name="user_session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STR,
    )
