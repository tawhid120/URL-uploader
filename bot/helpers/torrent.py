"""Torrent & magnet-link downloader using aria2c."""

import asyncio
import os
import re

from bot.config import DOWNLOAD_DIR

# Pattern to detect magnet links
_MAGNET_RE = re.compile(r"^magnet:\?xt=urn:", re.IGNORECASE)

# Pattern to detect .torrent URLs
_TORRENT_RE = re.compile(r"\.torrent(\?.*)?$", re.IGNORECASE)


def is_torrent_or_magnet(url: str) -> bool:
    """Return ``True`` if *url* is a magnet link or points to a .torrent file."""
    return bool(_MAGNET_RE.match(url) or _TORRENT_RE.search(url))


async def download_torrent(url: str, user_id: int = 0) -> list[str]:
    """Download a torrent/magnet using ``aria2c`` and return file paths.

    Requires ``aria2c`` to be installed on the system.  Returns an empty
    list if aria2c is not available or the download fails.
    """
    user_dir = os.path.join(DOWNLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    cmd = [
        "aria2c",
        "--seed-time=0",            # Don't seed after completion
        "--max-tries=3",
        "--retry-wait=5",
        "--dir", user_dir,
        "--summary-interval=0",
        "--bt-stop-timeout=120",
        "--allow-overwrite=true",
        url,
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.wait()
    except (FileNotFoundError, OSError):
        return []

    if proc.returncode != 0:
        return []

    # Collect all files that were downloaded into user_dir
    files: list[str] = []
    for root, _dirs, filenames in os.walk(user_dir):
        for fname in filenames:
            fpath = os.path.join(root, fname)
            # Skip aria2 control files
            if fname.endswith(".aria2"):
                continue
            files.append(fpath)

    return sorted(files)
