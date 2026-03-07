import os
import re

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.database.users import (
    ensure_user,
    get_user,
    get_daily_usage,
    increment_usage,
)
from bot.config import PLAN_LIMITS, DOWNLOAD_DIR
from bot.helpers.downloader import extract_info, build_format_list, download_media
from bot.helpers.keyboards import quality_keyboard
from bot.helpers.utils import human_bytes

# Simple URL regex
_URL_RE = re.compile(r"https?://\S+")

# In-memory store for pending URL selections: {user_id: {"url": ..., "info": ...}}
pending_urls: dict[int, dict] = {}


@Client.on_message(filters.text & filters.private & ~filters.command(
    ["start", "help", "settings", "myplan", "upgrade", "bulk", "abort",
     "cookie", "delcookie", "delthumb"]
))
async def url_handler(client: Client, message: Message):
    """Handle plain text messages that contain URLs."""
    url_match = _URL_RE.search(message.text or "")
    if not url_match:
        await message.reply_text("❌ Please send a valid URL.")
        return

    url = url_match.group(0)
    user = message.from_user
    await ensure_user(user.id, user.first_name)
    db_user = await get_user(user.id)
    if db_user is None:
        await message.reply_text("❌ An error occurred. Please try /start again.")
        return

    # Check daily limits
    plan = db_user.get("plan", "free")
    limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])
    usage = await get_daily_usage(user.id)

    if usage["files"] >= limits["files"]:
        await message.reply_text(
            "⚠️ **Daily file limit reached!**\n"
            "Use /upgrade to increase your limits."
        )
        return
    if usage["bandwidth"] >= limits["bandwidth"]:
        await message.reply_text(
            "⚠️ **Daily bandwidth limit reached!**\n"
            "Use /upgrade to increase your limits."
        )
        return

    status_msg = await message.reply_text("🔍 **Fetching info…** Please wait.")

    # Resolve cookie path
    cookie_path = None
    cookie_fid = db_user.get("cookie_file_id")
    if cookie_fid:
        cookie_path = os.path.join(DOWNLOAD_DIR, str(user.id), "cookies.txt")
        os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
        await client.download_media(cookie_fid, file_name=cookie_path)

    try:
        info = await extract_info(url, cookie_path)
    except Exception as exc:
        await status_msg.edit_text(f"❌ **Failed to fetch info:**\n`{exc}`")
        return

    title = info.get("title", "Unknown")
    duration = info.get("duration")
    dur_str = f"{int(duration // 60)}:{int(duration % 60):02d}" if duration else "N/A"

    formats = build_format_list(info)

    if formats:
        pending_urls[user.id] = {"url": url, "info": info, "cookie_path": cookie_path}
        await status_msg.edit_text(
            f"🎬 **{title}**\n⏱ Duration: {dur_str}\n\n"
            "👇 **Select quality:**",
            reply_markup=quality_keyboard(formats),
        )
    else:
        # No selectable formats — download best directly
        await status_msg.edit_text("⬇️ **Downloading…** Please wait.")
        await _do_download(client, message, status_msg, url, "best", cookie_path)


async def _do_download(
    client: Client,
    message: Message,
    status_msg: Message,
    url: str,
    format_id: str,
    cookie_path: str | None,
):
    """Download and upload the file to the user."""
    user = message.from_user
    try:
        file_path = await download_media(url, format_id, cookie_path, user.id)
    except Exception as exc:
        await status_msg.edit_text(f"❌ **Download failed:**\n`{exc}`")
        return

    if not file_path or not os.path.isfile(file_path):
        await status_msg.edit_text("❌ **File not found after download.**")
        return

    file_size = os.path.getsize(file_path)
    await status_msg.edit_text(
        f"📤 **Uploading…** ({human_bytes(file_size)})"
    )

    db_user = await get_user(user.id)
    thumb_fid = db_user.get("thumbnail") if db_user else None

    thumb_path = None
    if thumb_fid:
        thumb_path = os.path.join(DOWNLOAD_DIR, str(user.id), "thumb.jpg")
        await client.download_media(thumb_fid, file_name=thumb_path)

    try:
        if file_path.endswith(".mp3"):
            await client.send_audio(
                chat_id=message.chat.id,
                audio=file_path,
                thumb=thumb_path,
            )
        else:
            await client.send_video(
                chat_id=message.chat.id,
                video=file_path,
                thumb=thumb_path,
                supports_streaming=True,
            )
    except Exception:
        # Fallback: send as document
        await client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            thumb=thumb_path,
        )

    await increment_usage(user.id, file_size)
    await status_msg.delete()

    # Clean up downloaded file
    try:
        os.remove(file_path)
        if thumb_path and os.path.isfile(thumb_path):
            os.remove(thumb_path)
    except OSError:
        pass
