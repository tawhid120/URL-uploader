"""Entry-point for the URL Uploader Bot web application.

Running ``python -m bot`` starts a **uvicorn** HTTP server whose
FastAPI ``lifespan`` automatically starts and stops the Pyrogram
Telegram bot.  This makes the application deployable on any platform
that expects a long-running HTTP process (Render, Railway, Heroku,
Koyeb, etc.).
"""

import logging

# ---- configure logging FIRST so every subsequent import is captured ----
from bot.logging_config import setup_logging

setup_logging()

from bot.config import PORT  # noqa: E402

# Register all Pyrogram handlers by importing them.
import bot.handlers.commands.start  # noqa: F401, E402
import bot.handlers.commands.help  # noqa: F401, E402
import bot.handlers.commands.settings  # noqa: F401, E402
import bot.handlers.commands.myplan  # noqa: F401, E402
import bot.handlers.commands.upgrade  # noqa: F401, E402
import bot.handlers.upload.bulk  # noqa: F401, E402
import bot.handlers.upload.cookie  # noqa: F401, E402
import bot.handlers.upload.thumbnail  # noqa: F401, E402
import bot.handlers.admin.commands  # noqa: F401, E402
import bot.handlers.upload.url_handler  # noqa: F401, E402
import bot.handlers.callbacks  # noqa: F401, E402

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn

    from bot.dashboard import _get_app

    logger.info("Starting URL Uploader Bot as web application on port %s …", PORT)

    app = _get_app()
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
