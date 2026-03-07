"""Playlist / gallery download helpers.

Downloads every entry in a yt-dlp playlist and returns the list of
local file paths.
"""

import asyncio
import os
from typing import Any

import yt_dlp

from bot.config import DOWNLOAD_DIR


async def download_playlist(
    url: str,
    cookie_path: str | None = None,
    user_id: int = 0,
) -> list[str]:
    """Download all entries of a playlist and return local file paths."""
    user_dir = os.path.join(DOWNLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    output_template = os.path.join(user_dir, "%(title).50s.%(ext)s")

    opts: dict[str, Any] = {
        "outtmpl": output_template,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "noplaylist": False,  # allow playlist
        "format": "best",
    }

    if cookie_path and os.path.isfile(cookie_path):
        opts["cookiefile"] = cookie_path

    loop = asyncio.get_event_loop()
    downloaded: list[str] = []

    def _download() -> None:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                return

            entries = info.get("entries")
            if entries:
                for entry in entries:
                    if entry is None:
                        continue
                    path = ydl.prepare_filename(entry)
                    resolved = _resolve_path(path)
                    if resolved:
                        downloaded.append(resolved)
            else:
                # Single video (not really a playlist)
                path = ydl.prepare_filename(info)
                resolved = _resolve_path(path)
                if resolved:
                    downloaded.append(resolved)

    await loop.run_in_executor(None, _download)
    return downloaded


def _resolve_path(path: str) -> str | None:
    """Return *path* if it exists, or try common extensions."""
    if os.path.isfile(path):
        return path
    base, _ = os.path.splitext(path)
    for ext in (".mp4", ".mp3", ".webm", ".mkv"):
        candidate = base + ext
        if os.path.isfile(candidate):
            return candidate
    return None


def is_playlist_url(info: dict) -> bool:
    """Return ``True`` if *info* (from ``extract_info``) represents a playlist."""
    return bool(info.get("_type") == "playlist" or info.get("entries"))
