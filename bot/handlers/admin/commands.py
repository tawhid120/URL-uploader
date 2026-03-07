import asyncio
import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import ADMIN_IDS
from bot.database.users import ban_user, unban_user, get_all_user_ids

logger = logging.getLogger(__name__)


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client: Client, message: Message):
    if not _is_admin(message.from_user.id):
        return

    if not message.reply_to_message:
        return await message.reply_text(
            "📢 **Reply to a message** with /broadcast to send it to all users."
        )

    user_ids = await get_all_user_ids()
    logger.info("Broadcast started by admin %s to %s users.", message.from_user.id, len(user_ids))
    status_msg = await message.reply_text(
        f"📢 **Broadcasting to {len(user_ids)} users…**"
    )

    sent = 0
    failed = 0
    for uid in user_ids:
        try:
            await message.reply_to_message.copy(uid)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.1)  # avoid FloodWait

    await status_msg.edit_text(
        f"✅ **Broadcast complete!**\n"
        f"Sent: {sent} | Failed: {failed}"
    )
    logger.info("Broadcast complete: sent=%s failed=%s", sent, failed)


@Client.on_message(filters.command("ban") & filters.private)
async def ban_handler(_client: Client, message: Message):
    if not _is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.reply_text(
            "🔨 **Usage:** `/ban <user_id>`"
        )

    target = int(parts[1])
    await ban_user(target)
    logger.info("User %s banned by admin %s.", target, message.from_user.id)
    await message.reply_text(f"🚫 User `{target}` has been **banned**.")


@Client.on_message(filters.command("unban") & filters.private)
async def unban_handler(_client: Client, message: Message):
    if not _is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.reply_text(
            "✅ **Usage:** `/unban <user_id>`"
        )

    target = int(parts[1])
    await unban_user(target)
    logger.info("User %s unbanned by admin %s.", target, message.from_user.id)
    await message.reply_text(f"✅ User `{target}` has been **unbanned**.")
