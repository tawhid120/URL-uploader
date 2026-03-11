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
from bot.handlers import register_handlers  # noqa: E402

register_handlers()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn

    from bot.dashboard import _get_app

    logger.info("Starting URL Uploader Bot as web application on port %s …", PORT)

    app = _get_app()
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
