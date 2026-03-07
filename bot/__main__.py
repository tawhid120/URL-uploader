import logging

from bot.client import bot, user_session

# Register all handlers by importing them
import bot.handlers.start  # noqa: F401
import bot.handlers.help  # noqa: F401
import bot.handlers.settings  # noqa: F401
import bot.handlers.myplan  # noqa: F401
import bot.handlers.upgrade  # noqa: F401
import bot.handlers.bulk  # noqa: F401
import bot.handlers.cookie  # noqa: F401
import bot.handlers.thumbnail  # noqa: F401
import bot.handlers.admin  # noqa: F401
import bot.handlers.url_handler  # noqa: F401
import bot.handlers.callbacks  # noqa: F401

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting URL Uploader Bot…")
    if user_session:
        logger.info("User session detected — 4 GB uploads enabled.")
        user_session.start()
    bot.run()
