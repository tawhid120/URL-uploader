from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def settings_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for /settings."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🖼 Set Thumbnail", callback_data="set_thumb"),
                InlineKeyboardButton("❌ Del Thumbnail", callback_data="del_thumb"),
            ],
            [
                InlineKeyboardButton("🍪 Manage Cookies", callback_data="manage_cookies"),
            ],
            [
                InlineKeyboardButton("💎 Upgrade Plan", callback_data="show_upgrade"),
            ],
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="refresh_settings"),
            ],
        ]
    )


def cookie_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for /cookie."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📤 Upload Cookie", callback_data="upload_cookie"),
            ],
            [
                InlineKeyboardButton("🗑 Delete Cookie", callback_data="del_cookie"),
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_main"),
            ],
        ]
    )


def upgrade_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for /upgrade."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⭐ Basic", callback_data="plan_basic"),
                InlineKeyboardButton("🔷 Standard", callback_data="plan_standard"),
            ],
            [
                InlineKeyboardButton("💎 Pro", callback_data="plan_pro"),
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_main"),
            ],
        ]
    )


def quality_keyboard(formats: list[dict]) -> InlineKeyboardMarkup:
    """Build a quality-selection keyboard from yt-dlp format list."""
    buttons = []
    seen = set()
    for fmt in formats:
        label = fmt.get("label", "")
        fmt_id = fmt.get("format_id", "")
        if label and label not in seen:
            seen.add(label)
            buttons.append(
                [InlineKeyboardButton(label, callback_data=f"fmt|{fmt_id}")]
            )
    buttons.append(
        [InlineKeyboardButton("🎵 Audio Only", callback_data="fmt|audio")]
    )
    return InlineKeyboardMarkup(buttons)
