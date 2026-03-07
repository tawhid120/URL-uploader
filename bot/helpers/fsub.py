"""Force-subscribe middleware: ensure users join a channel before using the bot."""

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, PeerIdInvalid

from bot.config import FSUB_CHANNEL


async def check_fsub(client: Client, message: Message) -> bool:
    """Return True if the user has joined the FSub channel (or FSub is disabled).

    If the user has NOT joined, a prompt message is sent and False is returned.
    """
    if not FSUB_CHANNEL:
        return True

    try:
        channel = FSUB_CHANNEL
        if channel.lstrip("-").isdigit():
            channel = int(channel)
        await client.get_chat_member(channel, message.from_user.id)
        return True
    except UserNotParticipant:
        invite = f"https://t.me/{FSUB_CHANNEL}" if not str(FSUB_CHANNEL).lstrip("-").isdigit() else None
        buttons = []
        if invite:
            buttons.append([InlineKeyboardButton("📢 Join Channel", url=invite)])
        await message.reply_text(
            "🔒 **You must join our channel to use this bot.**\n\n"
            "Please join and try again.",
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
        )
        return False
    except (ChatAdminRequired, PeerIdInvalid):
        # Bot is not admin in the channel or channel misconfigured — skip check
        return True
