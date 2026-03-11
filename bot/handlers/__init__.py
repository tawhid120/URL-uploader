"""Handlers package for URL Uploader Bot.

Subpackages
-----------
commands — User-facing commands (start, help, settings, myplan, upgrade).
admin    — Admin-only commands (broadcast, ban, unban).
upload   — Content handling (URL download, bulk, cookie, thumbnail).

Modules
-------
callbacks — Inline callback-query handlers.
"""


def register_handlers() -> None:
    """Import all handler modules so Pyrogram decorators are registered."""
    import bot.handlers.commands.start  # noqa: F401
    import bot.handlers.commands.help  # noqa: F401
    import bot.handlers.commands.settings  # noqa: F401
    import bot.handlers.commands.myplan  # noqa: F401
    import bot.handlers.commands.upgrade  # noqa: F401
    import bot.handlers.upload.bulk  # noqa: F401
    import bot.handlers.upload.cookie  # noqa: F401
    import bot.handlers.upload.thumbnail  # noqa: F401
    import bot.handlers.admin.commands  # noqa: F401
    import bot.handlers.upload.url_handler  # noqa: F401
    import bot.handlers.callbacks  # noqa: F401
