from pyrogram import Client, filters
from pyrogram.types import Message

from bot.database.users import ensure_user, get_daily_usage
from bot.helpers.utils import human_bytes, plan_display
from bot.config import PLAN_LIMITS


@Client.on_message(filters.command("myplan") & filters.private)
async def myplan_handler(_client: Client, message: Message):
    user = message.from_user
    db_user = await ensure_user(user.id, user.first_name)
    usage = await get_daily_usage(user.id)

    plan = db_user.get("plan", "free")
    limit = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])
    bw_limit = human_bytes(limit["bandwidth"])
    bw_used = human_bytes(usage.get("bandwidth", 0))
    files_used = usage.get("files", 0)
    files_limit = limit["files"]
    files_limit_str = "∞" if files_limit == float("inf") else str(int(files_limit))

    joined = db_user.get("joined")
    joined_str = joined.strftime("%d %b %Y") if joined else "N/A"

    expiry = db_user.get("plan_expiry")
    if expiry:
        sub_line = f"⏰ Exᴘɪʀᴇs: {expiry.strftime('%d %b %Y')}"
    else:
        sub_line = "⏰ Nᴏ ᴀᴄᴛɪᴠᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ"

    # Benefits per plan
    benefits = {
        "free": "• 10 ғɪʟᴇs/ᴅᴀʏ\n• 2 GB/ᴅᴀʏ ʙᴀɴᴅᴡɪᴅᴛʜ",
        "basic": "• 50 ғɪʟᴇs/ᴅᴀʏ\n• 10 GB/ᴅᴀʏ ʙᴀɴᴅᴡɪᴅᴛʜ",
        "standard": "• 100 ғɪʟᴇs/ᴅᴀʏ\n• 30 GB/ᴅᴀʏ ʙᴀɴᴅᴡɪᴅᴛʜ",
        "pro": "• Uɴʟɪᴍɪᴛᴇᴅ ғɪʟᴇs\n• Uɴʟɪᴍɪᴛᴇᴅ ʙᴀɴᴅᴡɪᴅᴛʜ",
    }

    text = (
        "╭───────────⍟\n"
        "├ ＹＯＵＲ ＰＬＡＮ\n"
        "╰───────────────⍟\n\n"
        f"Sᴛᴀᴛᴜs: {plan_display(plan)}\n"
        f"{sub_line}\n\n"
        f"📊 Tᴏᴅᴀʏ Dᴏᴡɴʟᴏᴀᴅs: {files_used} / {files_limit_str}\n"
        f"📶 Bᴀɴᴅᴡɪᴅᴛʜ Usᴇᴅ: {bw_used} / {bw_limit}\n"
        f"📅 Jᴏɪɴᴇᴅ: {joined_str}\n\n"
        "━━━━  🎁 YOUR BENEFITS  ━━━━\n"
        f"{benefits.get(plan, benefits['free'])}"
    )
    await message.reply_text(text)
