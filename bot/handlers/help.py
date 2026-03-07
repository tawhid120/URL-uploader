from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("help") & filters.private)
async def help_handler(_client: Client, message: Message):
    text = (
        "╭───⍟ＵＲＬ ＵＰＬＯＡＤＥＲ⍟───╮\n\n"
        "𖣔 **Mᴀɪɴ Cᴏᴍᴍᴀɴᴅs**\n"
        "┣ /start - Iɴɪᴛɪᴀʟɪᴢᴇ Bᴏᴛ\n"
        "┣ /help - Usᴇʀ Gᴜɪᴅᴇ\n"
        "┣ /settings - Pʀᴇғᴇʀᴇɴᴄᴇs\n"
        "┣ /myplan - Usᴀɢᴇ Sᴛᴀᴛs\n"
        "┗ /upgrade - Pʀᴇᴍɪᴜᴍ Pʟᴀɴs\n\n"
        "𖣔 **Bᴜʟᴋ Mᴏᴅᴇ**\n"
        "┣ /bulk - Bᴀᴛᴄʜ Uᴘʟᴏᴀᴅ\n"
        "┗ /abort - Sᴛᴏᴘ Pʀᴏᴄᴇss\n\n"
        "𖣔 **Cᴏᴏᴋɪᴇ Aᴜᴛʜ**\n"
        "┣ /cookie - Aᴅᴅ Lᴏɢɪɴ\n"
        "┗ /delcookie - Wɪᴘᴇ Aᴜᴛʜ\n\n"
        "𖣔 **Cᴜsᴛᴏᴍɪᴢᴀᴛɪᴏɴ**\n"
        "┣ 📸 Photo - Sᴇᴛ Tʜᴜᴍʙ\n"
        "┗ /delthumb - Dᴇʟ Tʜᴜᴍʙ\n\n"
        "╰─━━━━━━━🥏━━━━━━━─╯\n\n"
        "💡 **Tɪᴘ:** Usᴇ ᴄᴏᴏᴋɪᴇs ғᴏʀ ʀᴇsᴛʀɪᴄᴛᴇᴅ sɪᴛᴇs."
    )
    await message.reply_text(text)
