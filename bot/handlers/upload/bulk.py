import asyncio
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
from bot.config import PLAN_LIMITS, DOWNLOAD_DIR
from bot.helpers.download import download_media
from bot.helpers.utils import human_bytes
from bot.helpers.fsub import check_fsub

_URL_RE = re.compile(r"https?://\S+")

# Per-user bulk queues and abort flags
_bulk_queues: dict[int, asyncio.Queue] = {}
_bulk_abort: dict[int, bool] = {}

MAX_BULK_LINKS = 200
PROGRESS_UPDATE_INTERVAL = 3


@Client.on_message(filters.command("bulk") & filters.private)
async def bulk_handler(client: Client, message: Message):
    user = message.from_user
    await ensure_user(user.id, user.first_name)

    if await is_banned(user.id):
        return await message.reply_text("🚫 **You are banned from using this bot.**")

    if not await check_fsub(client, message):
        return

    db_user = await get_user(user.id)
    plan = (db_user or {}).get("plan", "free")
    if plan == "free":
        return await message.reply_text(
            "🔒 **Bulk Mode is a Premium Feature**\n\n"
            "Use /upgrade to unlock bulk uploads (up to 200 links at once)!"
        )

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply_text(
            "📝 **Usage:** `/bulk <links>`\n\n"
            "Send up to 200 URLs separated by newlines.\n"
            "Example:\n"
            "`/bulk\nhttps://example.com/video1\nhttps://example.com/video2`"
        )

    raw_links = parts[1].strip().splitlines()
    urls = [u.strip() for u in raw_links if _URL_RE.match(u.strip())]

    if not urls:
        return await message.reply_text("❌ No valid URLs found in your message.")

    if len(urls) > MAX_BULK_LINKS:
        urls = urls[:MAX_BULK_LINKS]

    _bulk_abort[user.id] = False
    queue: asyncio.Queue = asyncio.Queue()
    _bulk_queues[user.id] = queue
    for url in urls:
        await queue.put(url)

    total = len(urls)
    progress_msg = await message.reply_text(
        f"📦 **Bulk Mode Started**\n"
        f"Total links: {total}\n"
        f"Progress: 0 / {total}\n"
        "Use /abort to cancel."
    )

    done = 0
    failed = 0
    limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])

    # Resolve cookie path once
    cookie_path = None
    cookie_fid = (db_user or {}).get("cookie_file_id")
    if cookie_fid:
        cookie_path = os.path.join(DOWNLOAD_DIR, str(user.id), "cookies.txt")
        os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
        await client.download_media(cookie_fid, file_name=cookie_path)

    while not queue.empty():
        if _bulk_abort.get(user.id):
            await progress_msg.edit_text(
                f"⛔ **Bulk process aborted!**\n"
                f"Completed: {done} / {total} | Failed: {failed}"
            )
            _cleanup_bulk(user.id)
            return

        url = await queue.get()

        # Check daily limits
        usage = await get_daily_usage(user.id)
        if usage["files"] >= limits["files"] or usage["bandwidth"] >= limits["bandwidth"]:
            await progress_msg.edit_text(
                f"⚠️ **Daily limit reached during bulk!**\n"
                f"Completed: {done} / {total} | Failed: {failed}"
            )
            _cleanup_bulk(user.id)
            return

        try:
            file_path = await download_media(url, "best", cookie_path, user.id)
            if file_path and os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                try:
                    await client.send_document(
                        chat_id=message.chat.id,
                        document=file_path,
                    )
                except Exception:
                    failed += 1
                else:
                    await increment_usage(user.id, file_size)
                    done += 1
                finally:
                    try:
                        os.remove(file_path)
                    except OSError:
                        pass
            else:
                failed += 1
        except Exception:
            failed += 1

        # Update progress periodically or at the end
        if done % PROGRESS_UPDATE_INTERVAL == 0 or queue.empty():
            try:
                await progress_msg.edit_text(
                    f"📦 **Bulk Mode**\n"
                    f"Progress: {done + failed} / {total}\n"
                    f"✅ Done: {done} | ❌ Failed: {failed}"
                )
            except Exception:
                pass

    await progress_msg.edit_text(
        f"✅ **Bulk upload complete!**\n"
        f"Total: {total} | ✅ Done: {done} | ❌ Failed: {failed}"
    )
    _cleanup_bulk(user.id)


@Client.on_message(filters.command("abort") & filters.private)
async def abort_handler(_client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in _bulk_queues:
        _bulk_abort[user_id] = True
        await message.reply_text("⛔ **Aborting bulk process…**")
    else:
        await message.reply_text("⛔ **No active bulk process to stop.**")


def _cleanup_bulk(user_id: int) -> None:
    _bulk_queues.pop(user_id, None)
    _bulk_abort.pop(user_id, None)
