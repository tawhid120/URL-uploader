"""Tests for bot.helpers.thumbnail module."""

import asyncio
import os
import tempfile

from bot.helpers.thumbnail import generate_thumbnail


class TestGenerateThumbnail:
    """Unit tests for the auto-thumbnail generator."""

    def test_nonexistent_file_returns_none(self):
        result = asyncio.get_event_loop().run_until_complete(
            generate_thumbnail("/tmp/does_not_exist.mp4")
        )
        assert result is None

    def test_invalid_video_returns_none(self):
        """A file with no video stream should return None."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"\x00" * 100)
            f.flush()
            path = f.name

        try:
            result = asyncio.get_event_loop().run_until_complete(
                generate_thumbnail(path)
            )
            # FFmpeg will likely fail on a dummy file
            assert result is None
        finally:
            os.unlink(path)
