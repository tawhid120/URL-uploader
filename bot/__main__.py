import logging

from bot.client import bot, user_session

# Register all handlers by importing them
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting URL Uploader Bot…")

    # Start the optional admin web dashboard
    from bot.dashboard import start_dashboard
    start_dashboard()

    if user_session:
        logger.info("User session detected — 4 GB uploads enabled.")
        user_session.start()
    bot.run()
