"""FFmpeg auto-split utility for files exceeding Telegram's upload limit."""

import asyncio
import os
import math


async def split_file(file_path: str, chunk_size: int) -> list[str]:
    """Split a video/audio file into chunks of at most *chunk_size* bytes.

    Uses FFmpeg segment muxer to produce time-based splits whose individual
    sizes are approximately *chunk_size*.

    Returns a sorted list of output file paths.
    """
    total_size = os.path.getsize(file_path)
    if total_size <= chunk_size:
        return [file_path]

    # Estimate segment duration from total duration & desired chunk count
    num_parts = math.ceil(total_size / chunk_size)

    # Probe duration with ffprobe
    duration = await _probe_duration(file_path)
    if duration <= 0:
        return [file_path]  # cannot split without duration info

    segment_time = int(duration / num_parts) or 1

    base, ext = os.path.splitext(file_path)
    pattern = f"{base}_part%03d{ext}"

    cmd = [
        "ffmpeg", "-y", "-i", file_path,
        "-c", "copy",
        "-map", "0",
        "-f", "segment",
        "-segment_time", str(segment_time),
        "-reset_timestamps", "1",
        pattern,
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()
    except (FileNotFoundError, OSError):
        return [file_path]

    # Collect output parts
    parts: list[str] = sorted(
        os.path.join(os.path.dirname(file_path), f)
        for f in os.listdir(os.path.dirname(file_path))
        if f.startswith(os.path.basename(base) + "_part") and f.endswith(ext)
    )

    return parts if parts else [file_path]


async def _probe_duration(file_path: str) -> float:
    """Return the duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await proc.communicate()
        return float(stdout.decode().strip())
    except (ValueError, AttributeError, FileNotFoundError, OSError):
        return 0.0
