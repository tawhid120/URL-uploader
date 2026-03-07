from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("bulk") & filters.private)
async def bulk_handler(_client: Client, message: Message):
    text = (
        "🔒 **Bulk Mode is a Premium Feature**\n\n"
        "Use /upgrade to unlock bulk uploads (up to 200 links at once)!"
    )
    await message.reply_text(text)


@Client.on_message(filters.command("abort") & filters.private)
async def abort_handler(_client: Client, message: Message):
    await message.reply_text("⛔ **Process aborted.** No active downloads to stop.")
