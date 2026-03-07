import logging
import os
import re

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.database.users import (
    ensure_user,
    get_user,
    get_daily_usage,
    increment_usage,
    is_banned,
)
from bot.config import (
    PLAN_LIMITS,
    DOWNLOAD_DIR,
    TG_BOT_FILE_LIMIT,
    TG_USER_FILE_LIMIT,
    TG_SPLIT_SIZE,
)
from bot.client import user_session
from bot.helpers.download import (
    extract_info,
    build_format_list,
    download_media,
    is_torrent_or_magnet,
    download_torrent,
    download_playlist,
    is_playlist_url,
)
from bot.helpers.keyboards import quality_keyboard
from bot.helpers.utils import human_bytes
from bot.helpers.fsub import check_fsub
from bot.helpers.media import split_file, generate_thumbnail, create_zip

logger = logging.getLogger(__name__)

# Simple URL regex
_URL_RE = re.compile(r"https?://\S+")

# In-memory store for pending URL selections: {user_id: {"url": ..., "info": ...}}
pending_urls: dict[int, dict] = {}


@Client.on_message(filters.text & filters.private & ~filters.command(
    ["start", "help", "settings", "myplan", "upgrade", "bulk", "abort",
     "cookie", "delcookie", "delthumb", "broadcast", "ban", "unban"]
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
    logger.info("URL received from user %s (%s): %s", user.id, user.first_name, url)

    if await is_banned(user.id):
        return await message.reply_text("🚫 **You are banned from using this bot.**")

    if not await check_fsub(client, message):
        return

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

    # ---- Torrent / Magnet shortcut ----
    if is_torrent_or_magnet(url):
        logger.info("Torrent/magnet detected for user %s: %s", user.id, url)
        await status_msg.edit_text("🧲 **Downloading torrent…** This may take a while.")
        files = await download_torrent(url, user.id)
        if not files:
            logger.warning("Torrent download failed for user %s: %s", user.id, url)
            return await status_msg.edit_text("❌ **Torrent download failed.**\nMake sure `aria2c` is installed.")
        total_size = sum(os.path.getsize(f) for f in files)
        for fpath in files:
            try:
                await client.send_document(chat_id=message.chat.id, document=fpath)
            except Exception:
                pass
        await increment_usage(user.id, total_size)
        await status_msg.delete()
        for fpath in files:
            try:
                os.remove(fpath)
            except OSError:
                pass
        return

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
        logger.error("Failed to extract info for %s (user %s): %s", url, user.id, exc)
        await status_msg.edit_text(f"❌ **Failed to fetch info:**\n`{exc}`")
        return

    # ---- Playlist / gallery → ZIP ----
    if is_playlist_url(info):
        await status_msg.edit_text("📦 **Downloading playlist…** Please wait.")
        try:
            files = await download_playlist(url, cookie_path, user.id)
        except Exception as exc:
            return await status_msg.edit_text(f"❌ **Playlist download failed:**\n`{exc}`")
        if not files:
            return await status_msg.edit_text("❌ **No files downloaded from playlist.**")
        title = info.get("title", "playlist")
        zip_path = os.path.join(DOWNLOAD_DIR, str(user.id), f"{title[:50]}.zip")
        create_zip(files, zip_path)
        zip_size = os.path.getsize(zip_path)
        await status_msg.edit_text(f"📤 **Uploading ZIP** ({human_bytes(zip_size)})")
        try:
            await client.send_document(chat_id=message.chat.id, document=zip_path, caption=f"📦 {title}")
        except Exception as exc:
            await status_msg.edit_text(f"❌ **Upload failed:**\n`{exc}`")
        else:
            await increment_usage(user.id, zip_size)
            await status_msg.delete()
        for fpath in files:
            try:
                os.remove(fpath)
            except OSError:
                pass
        try:
            os.remove(zip_path)
        except OSError:
            pass
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
    logger.info("Starting download for user %s: url=%s format=%s", user.id, url, format_id)
    try:
        file_path = await download_media(url, format_id, cookie_path, user.id)
    except Exception as exc:
        logger.error("Download failed for user %s: %s", user.id, exc)
        await status_msg.edit_text(f"❌ **Download failed:**\n`{exc}`")
        return

    if not file_path or not os.path.isfile(file_path):
        await status_msg.edit_text("❌ **File not found after download.**")
        return

    file_size = os.path.getsize(file_path)
    logger.info(
        "Download complete for user %s: %s (%s)",
        user.id, os.path.basename(file_path), human_bytes(file_size),
    )
    await status_msg.edit_text(
        f"📤 **Uploading…** ({human_bytes(file_size)})"
    )

    db_user = await get_user(user.id)
    thumb_fid = db_user.get("thumbnail") if db_user else None
    custom_caption = db_user.get("caption") if db_user else None
    plan = (db_user or {}).get("plan", "free")

    thumb_path = None
    if thumb_fid:
        thumb_path = os.path.join(DOWNLOAD_DIR, str(user.id), "thumb.jpg")
        await client.download_media(thumb_fid, file_name=thumb_path)
    elif file_path.endswith((".mp4", ".mkv", ".webm", ".avi", ".mov", ".flv")):
        # Auto-generate thumbnail from video when user hasn't set one
        thumb_path = await generate_thumbnail(file_path)

    caption = custom_caption or os.path.basename(file_path)

    # Determine if we need to split the file
    upload_limit = TG_BOT_FILE_LIMIT
    uploader = client
    if user_session and plan in ("basic", "standard", "pro"):
        upload_limit = TG_USER_FILE_LIMIT
        uploader = user_session

    files_to_upload: list[str] = [file_path]
    if file_size > upload_limit:
        # Leave a 1 MB buffer for Telegram metadata overhead
        split_chunk = TG_SPLIT_SIZE if uploader == client else TG_USER_FILE_LIMIT - 1024**2
        files_to_upload = await split_file(file_path, split_chunk)

    for idx, fpath in enumerate(files_to_upload):
        part_caption = f"{caption} (Part {idx + 1}/{len(files_to_upload)})" if len(files_to_upload) > 1 else caption
        try:
            await _upload_file(uploader, message.chat.id, fpath, thumb_path, part_caption)
        except Exception:
            # Fallback to bot client if user session fails
            if uploader != client:
                try:
                    await _upload_file(client, message.chat.id, fpath, thumb_path, part_caption)
                except Exception:
                    await client.send_document(
                        chat_id=message.chat.id,
                        document=fpath,
                        thumb=thumb_path,
                        caption=part_caption,
                    )
            else:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=fpath,
                    thumb=thumb_path,
                    caption=part_caption,
                )

    await increment_usage(user.id, file_size)
    logger.info("Upload complete for user %s: %s", user.id, os.path.basename(file_path))
    await status_msg.delete()

    # Clean up downloaded files
    for fpath in files_to_upload:
        try:
            os.remove(fpath)
        except OSError:
            pass
    # When splitting occurred the original file differs from the parts
    if file_path not in files_to_upload:
        try:
            os.remove(file_path)
        except OSError:
            pass
    if thumb_path and os.path.isfile(thumb_path):
        try:
            os.remove(thumb_path)
        except OSError:
            pass


async def _upload_file(
    uploader: Client,
    chat_id: int,
    file_path: str,
    thumb_path: str | None,
    caption: str,
) -> None:
    """Upload a single file as video, audio, or document."""
    if file_path.endswith(".mp3"):
        await uploader.send_audio(
            chat_id=chat_id,
            audio=file_path,
            thumb=thumb_path,
            caption=caption,
        )
    else:
        await uploader.send_video(
            chat_id=chat_id,
            video=file_path,
            thumb=thumb_path,
            caption=caption,
            supports_streaming=True,
        )
