from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers.keyboards import upgrade_keyboard


@Client.on_message(filters.command("upgrade") & filters.private)
async def upgrade_handler(_client: Client, message: Message):
    text = (
        "╭─❖ **PREMIUM PLANS** ❖─╮\n\n"
        "⭐ **BASIC**\n"
        "│ 📁 50 files / day\n"
        "│ 📶 10 GB daily bandwidth\n"
        "├─────────────────\n\n"
        "🔷 **STANDARD**\n"
        "│ 📁 100 files / day\n"
        "│ 📶 30 GB daily bandwidth\n"
        "├─────────────────\n\n"
        "💎 **PRO**\n"
        "│ 📁 Unlimited files\n"
        "│ 📶 Unlimited bandwidth\n"
        "╰─────────────────╯\n\n"
        "👇 **Select a plan below to continue**"
    )
    await message.reply_text(text, reply_markup=upgrade_keyboard())
