from pyrogram import Client, filters
from pyrogram.types import Message

from bot.database.users import ensure_user, get_daily_usage
from bot.helpers.keyboards import settings_keyboard
from bot.helpers.utils import human_bytes, plan_display
from bot.config import PLAN_LIMITS


@Client.on_message(filters.command("settings") & filters.private)
async def settings_handler(_client: Client, message: Message):
    user = message.from_user
    db_user = await ensure_user(user.id, user.first_name)
    usage = await get_daily_usage(user.id)

    plan = db_user.get("plan", "free")
    limit = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])
    bw_limit = human_bytes(limit["bandwidth"])
    bw_used = human_bytes(usage.get("bandwidth", 0))
    thumb = "✅ Set" if db_user.get("thumbnail") else "❌ Not set"
    caption = "✅ Set" if db_user.get("caption") else "❌ Not set"

    text = (
        "⚙️ **YOUR SETTINGS**\n\n"
        f"👤 **Account Tier:** {plan_display(plan)}\n"
        f"📊 **Today's Usage:** {bw_used} / {bw_limit}\n"
        f"🖼 **Custom Thumbnail:** {thumb}\n"
        f"✏️ **Custom Caption:** {caption}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Manage your settings using the buttons below."
    )
    await message.reply_text(text, reply_markup=settings_keyboard())
