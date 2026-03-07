from pyrogram import Client, filters
from pyrogram.types import Message

from bot.database.users import ensure_user, set_cookie
from bot.helpers.keyboards import cookie_keyboard


@Client.on_message(filters.command("cookie") & filters.private)
async def cookie_handler(_client: Client, message: Message):
    await ensure_user(message.from_user.id, message.from_user.first_name)
    text = (
        "🍪 **Cookie Control Panel**\n\n"
        "Upload cookies to bypass login walls and age restrictions "
        "for virtually any website, including:\n"
        "• YouTube\n"
        "• Instagram\n"
        "• TikTok\n"
        "• XHamster\n"
        "• Twitter / X\n"
        "• Hotstar & more!\n\n"
        "🛠 **How to get cookies:**\n"
        " 1. Install the **Cookie-Editor** extension in your PC/Mobile browser.\n"
        " 2. Go to the website you want to download from "
        "(e.g. youtube.com) and log in.\n"
        " 3. Click the **Cookie-Editor** extension button.\n"
        " 4. Click **Export** ➔ **Export as Netscape** "
        "(Format must be Netscape!).\n"
        " 5. Paste the copied text into a new text file and save it as "
        "`cookies.txt`.\n\n"
        "Select an option below to manage your cookies:"
    )
    await message.reply_text(text, reply_markup=cookie_keyboard())


@Client.on_message(filters.command("delcookie") & filters.private)
async def delcookie_handler(_client: Client, message: Message):
    await set_cookie(message.from_user.id, None)
    await message.reply_text("🗑 **Cookie deleted successfully!**")
