"""Centralized logging configuration for the URL Uploader Bot.

Ensures that all bot activity — Pyrogram events, handler actions,
download/upload progress, and web server requests — is logged
consistently through both console output and an in-memory ring buffer
accessible via the ``/logs`` dashboard endpoint.
"""

import collections
import logging
from logging import Handler


class MemoryLogHandler(Handler):
    """A logging handler that stores recent log records in a ring buffer.

    This allows the web dashboard to display recent bot activity
    without needing access to log files on the host.
    """

    def __init__(self, capacity: int = 500):
        super().__init__()
        self.buffer: collections.deque[str] = collections.deque(maxlen=capacity)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.buffer.append(self.format(record))
        except Exception:
            self.handleError(record)

    def get_logs(self, count: int = 100) -> list[str]:
        """Return the last *count* log lines."""
        return list(self.buffer)[-count:]

    def clear(self) -> None:
        self.buffer.clear()


# Shared instance used by the dashboard /logs endpoint.
memory_handler = MemoryLogHandler(capacity=1000)


def setup_logging() -> None:
    """Configure logging for the entire application.

    * Console handler — all INFO+ messages go to *stderr*.
    * Memory handler — same messages are kept in a ring buffer for the
      ``/logs`` dashboard endpoint.
    * Noisy library loggers (uvicorn access, pyrogram internals) are
      quieted to WARNING so bot-specific messages stand out.
    """
    fmt = "%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(fmt, datefmt=datefmt)

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # Memory handler (for dashboard)
    memory_handler.setFormatter(formatter)

    # Root logger
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(console)
    root.addHandler(memory_handler)

    # Reduce noise from library internals
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.session").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.connection").setLevel(logging.WARNING)
