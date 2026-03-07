import os

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from bot.database.users import (
    ensure_user,
    get_user,
    get_daily_usage,
    set_thumbnail,
    set_cookie,
    set_caption,
)
from bot.config import PLAN_LIMITS, DOWNLOAD_DIR
from bot.helpers.keyboards import (
    settings_keyboard,
    cookie_keyboard,
    upgrade_keyboard,
)
from bot.helpers.utils import human_bytes, plan_display
from bot.handlers.url_handler import pending_urls, _do_download
from bot.helpers.cookie_validator import validate_cookies


@Client.on_callback_query(filters.regex(r"^set_thumb$"))
async def cb_set_thumb(_client: Client, cb: CallbackQuery):
    await cb.answer()
    await cb.message.reply_text("📸 **Send me a photo** to set as your custom thumbnail.")


@Client.on_callback_query(filters.regex(r"^del_thumb$"))
async def cb_del_thumb(_client: Client, cb: CallbackQuery):
    await set_thumbnail(cb.from_user.id, None)
    await cb.answer("Thumbnail removed!", show_alert=True)


@Client.on_callback_query(filters.regex(r"^manage_cookies$"))
async def cb_manage_cookies(_client: Client, cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_text(
        "🍪 **Cookie Management**\n\n"
        "Choose an action below:",
        reply_markup=cookie_keyboard(),
    )


@Client.on_callback_query(filters.regex(r"^upload_cookie$"))
async def cb_upload_cookie(_client: Client, cb: CallbackQuery):
    await cb.answer()
    await cb.message.reply_text(
        "📤 **Send your cookies.txt file** as a document.\n"
        "Make sure it's in **Netscape** format!"
    )


@Client.on_callback_query(filters.regex(r"^del_cookie$"))
async def cb_del_cookie(_client: Client, cb: CallbackQuery):
    await set_cookie(cb.from_user.id, None)
    await cb.answer("Cookie deleted!", show_alert=True)


@Client.on_callback_query(filters.regex(r"^show_upgrade$"))
async def cb_show_upgrade(_client: Client, cb: CallbackQuery):
    await cb.answer()
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
    await cb.message.edit_text(text, reply_markup=upgrade_keyboard())


@Client.on_callback_query(filters.regex(r"^plan_(basic|standard|pro)$"))
async def cb_plan_select(_client: Client, cb: CallbackQuery):
    plan = cb.data.split("_", 1)[1]
    await cb.answer(
        f"✅ You selected {plan.title()} plan!\n"
        "Contact the admin to complete payment.",
        show_alert=True,
    )


@Client.on_callback_query(filters.regex(r"^refresh_settings$"))
async def cb_refresh_settings(_client: Client, cb: CallbackQuery):
    user = cb.from_user
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
    await cb.message.edit_text(text, reply_markup=settings_keyboard())
    await cb.answer("Refreshed!")


@Client.on_callback_query(filters.regex(r"^back_main$"))
async def cb_back_main(_client: Client, cb: CallbackQuery):
    await cb.answer()
    user = cb.from_user
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
    await cb.message.edit_text(text, reply_markup=settings_keyboard())


@Client.on_callback_query(filters.regex(r"^fmt\|"))
async def cb_format_select(client: Client, cb: CallbackQuery):
    """Handle quality/format selection from the inline keyboard."""
    await cb.answer()
    user_id = cb.from_user.id
    data = pending_urls.get(user_id)
    if not data:
        await cb.message.edit_text("❌ Session expired. Please send the URL again.")
        return

    format_id = cb.data.split("|", 1)[1]
    url = data["url"]
    cookie_path = data.get("cookie_path")
    pending_urls.pop(user_id, None)

    status_msg = await cb.message.edit_text("⬇️ **Downloading…** Please wait.")

    # We need the original message for sending the file back — use the callback message
    await _do_download(client, cb.message, status_msg, url, format_id, cookie_path)


# In-memory flag for users awaiting caption input
_awaiting_caption: set[int] = set()


@Client.on_callback_query(filters.regex(r"^set_caption$"))
async def cb_set_caption(_client: Client, cb: CallbackQuery):
    await cb.answer()
    _awaiting_caption.add(cb.from_user.id)
    await cb.message.reply_text(
        "✏️ **Send me the caption text** you want to use.\n\n"
        "You can use `{filename}` as a placeholder for the file name."
    )


@Client.on_callback_query(filters.regex(r"^del_caption$"))
async def cb_del_caption(_client: Client, cb: CallbackQuery):
    await set_caption(cb.from_user.id, None)
    await cb.answer("Caption removed!", show_alert=True)


@Client.on_message(filters.document & filters.private)
async def document_handler(client: Client, message):
    """Handle document uploads — specifically cookie files."""
    file_name = message.document.file_name or ""
    if file_name.endswith(".txt"):
        user = message.from_user
        await ensure_user(user.id, user.first_name)

        # Download temporarily to validate
        tmp_path = os.path.join(DOWNLOAD_DIR, str(user.id), "cookies_tmp.txt")
        os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
        await client.download_media(message.document.file_id, file_name=tmp_path)

        status = await message.reply_text("🔍 **Validating cookie…** Please wait.")
        valid = await validate_cookies(tmp_path)

        # Clean up temp file
        try:
            os.remove(tmp_path)
        except OSError:
            pass

        if not valid:
            await status.edit_text(
                "❌ **Cookie validation failed!**\n"
                "The cookie file appears to be invalid or expired.\n"
                "Please export a fresh cookie and try again."
            )
            return

        # Cookie is valid — save it
        await set_cookie(user.id, message.document.file_id)
        await status.edit_text("✅ **Cookie file saved!** Validation passed — it will be used for future downloads.")
    else:
        await message.reply_text(
            "📄 Please send a **.txt** file (Netscape cookie format)."
        )
