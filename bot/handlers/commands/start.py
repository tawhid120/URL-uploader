import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.database.users import ensure_user, is_banned
from bot.helpers.fsub import check_fsub

logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user = message.from_user
    await ensure_user(user.id, user.first_name)
    logger.info("/start from user %s (%s)", user.id, user.first_name)

    if await is_banned(user.id):
        return await message.reply_text("🚫 **You are banned from using this bot.**")

    if not await check_fsub(client, message):
        return

    text = (
        f"🌟 **Welcome to URL Uploader Bot, {user.first_name}!** 🌟\n\n"
        "🚀 **What I Can Do:**\n"
        "🔗 Download from YouTube, Instagram, TikTok, Twitter & more\n"
        "🎬 Choose exact video quality (1080p, 720p, 480p…)\n"
        "🎵 Extract audio from any video\n"
        "🖼 Download image galleries\n"
        "🍪 Cookie-based auth for restricted content\n\n"
        "💎 **Upgrade for more power:**\n"
        "🔹 ⭐ Basic — 50 files/day, 10 GB\n"
        "🔹 🔷 Standard — 100 files/day, 30 GB\n"
        "🔹 💎 Pro — Unlimited everything\n\n"
        "📌 **Send a link to get started!** 😊"
    )
    await message.reply_text(text)
