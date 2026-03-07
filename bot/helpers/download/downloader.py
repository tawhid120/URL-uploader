import os
import asyncio
from typing import Any

import yt_dlp

from bot.config import DOWNLOAD_DIR


async def extract_info(url: str, cookie_path: str | None = None) -> dict[str, Any]:
    """Extract video/audio info without downloading."""
    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    if cookie_path and os.path.isfile(cookie_path):
        opts["cookiefile"] = cookie_path

    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = await loop.run_in_executor(None, ydl.extract_info, url, False)
    return info or {}


def build_format_list(info: dict) -> list[dict]:
    """Build a simplified list of available video formats."""
    formats = info.get("formats") or []
    results: list[dict] = []
    for f in formats:
        height = f.get("height")
        ext = f.get("ext", "mp4")
        fmt_id = f.get("format_id", "")
        if height and ext in ("mp4", "webm"):
            label = f"{height}p — {ext}"
            results.append({"label": label, "format_id": fmt_id, "height": height})
    # Sort descending by quality
    results.sort(key=lambda x: x.get("height", 0), reverse=True)
    return results


async def download_media(
    url: str,
    format_id: str = "best",
    cookie_path: str | None = None,
    user_id: int = 0,
) -> str:
    """Download media and return the file path."""
    user_dir = os.path.join(DOWNLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    output_template = os.path.join(user_dir, "%(title).50s.%(ext)s")

    opts: dict[str, Any] = {
        "outtmpl": output_template,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "noplaylist": True,
    }

    if format_id == "audio":
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ]
        output_template = os.path.join(user_dir, "%(title).50s.%(ext)s")
        opts["outtmpl"] = output_template
    else:
        opts["format"] = f"{format_id}+bestaudio/best"

    if cookie_path and os.path.isfile(cookie_path):
        opts["cookiefile"] = cookie_path

    loop = asyncio.get_event_loop()

    downloaded_path: str = ""

    def _download():
        nonlocal downloaded_path
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                downloaded_path = ydl.prepare_filename(info)

    await loop.run_in_executor(None, _download)
    # yt-dlp may have changed the extension after merge/post-processing
    if downloaded_path and not os.path.isfile(downloaded_path):
        base, _ = os.path.splitext(downloaded_path)
        for ext in (".mp4", ".mp3", ".webm", ".mkv"):
            candidate = base + ext
            if os.path.isfile(candidate):
                downloaded_path = candidate
                break
    return downloaded_path
