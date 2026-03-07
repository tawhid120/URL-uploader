"""Auto-thumbnail generator using FFmpeg.

Captures a screenshot from the midpoint (or at 10 seconds) of a video file
when no custom thumbnail has been set by the user.
"""

import asyncio
import os

from bot.helpers.split import _probe_duration


async def generate_thumbnail(video_path: str) -> str | None:
    """Generate a JPEG thumbnail from *video_path*.

    Strategy:
    - Probe the video duration.
    - Seek to the midpoint (or 10 s if the duration is unknown / very short).
    - Capture a single frame scaled to 320 px wide (preserving aspect ratio).

    Returns the path to the generated thumbnail, or ``None`` on failure.
    """
    if not os.path.isfile(video_path):
        return None

    duration = await _probe_duration(video_path)
    if duration > 0:
        seek = duration / 2
    else:
        seek = 10.0

    base, _ = os.path.splitext(video_path)
    thumb_path = f"{base}_thumb.jpg"

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(seek),
        "-i", video_path,
        "-vframes", "1",
        "-vf", "scale=320:-1",
        "-q:v", "5",
        thumb_path,
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()
    except (FileNotFoundError, OSError):
        return None

    if os.path.isfile(thumb_path) and os.path.getsize(thumb_path) > 0:
        return thumb_path
    return None
