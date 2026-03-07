from pyrogram import Client, filters
from pyrogram.types import Message

from bot.database.users import ensure_user, set_thumbnail


@Client.on_message(filters.photo & filters.private)
async def thumbnail_handler(_client: Client, message: Message):
    """Save a photo as the user's custom thumbnail."""
    await ensure_user(message.from_user.id, message.from_user.first_name)
    file_id = message.photo.file_id
    await set_thumbnail(message.from_user.id, file_id)
    await message.reply_text("📸 **Custom thumbnail set!**")


@Client.on_message(filters.command("delthumb") & filters.private)
async def delthumb_handler(_client: Client, message: Message):
    """Delete the user's custom thumbnail."""
    await set_thumbnail(message.from_user.id, None)
    await message.reply_text("🗑 **Thumbnail removed.**")
