"""Tests for bot.helpers.split module."""

import asyncio
import os
import tempfile

from bot.helpers.split import split_file, _probe_duration


class TestSplitFileSmall:
    """Test that files under the chunk size are returned as-is."""

    def test_small_file_not_split(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"\x00" * 100)
            f.flush()
            path = f.name

        try:
            result = asyncio.get_event_loop().run_until_complete(
                split_file(path, 1024)
            )
            assert result == [path]
        finally:
            os.unlink(path)


class TestProbeDuration:
    def test_invalid_file_returns_zero(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"\x00" * 10)
            f.flush()
            path = f.name

        try:
            dur = asyncio.get_event_loop().run_until_complete(
                _probe_duration(path)
            )
            assert dur == 0.0
        finally:
            os.unlink(path)
