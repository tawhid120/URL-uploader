"""Smart cookie validator using yt-dlp.

Validates a Netscape-format cookie file by attempting to extract info
for a known YouTube video.  If the cookie is expired or invalid the
extraction will fail, and we can inform the user immediately.
"""

import asyncio
import os
from typing import Any

import yt_dlp


# A short, publicly-available YouTube video used only for a HEAD-style check.
_TEST_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


async def validate_cookies(cookie_path: str) -> bool:
    """Return ``True`` if *cookie_path* lets yt-dlp access a test video.

    The check only extracts metadata (no download) so it is lightweight.
    """
    if not cookie_path or not os.path.isfile(cookie_path):
        return False

    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "cookiefile": cookie_path,
        "socket_timeout": 15,
    }

    loop = asyncio.get_event_loop()

    def _check() -> bool:
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(_TEST_URL, download=False)
                return info is not None and "title" in info
        except Exception:
            return False

    return await loop.run_in_executor(None, _check)
