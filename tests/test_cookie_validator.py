"""Tests for bot.helpers.cookie_validator module (structure only, no network)."""

import asyncio
import os
import tempfile

from bot.helpers.cookie import validate_cookies


class TestValidateCookiesInput:
    """Test input validation — no network calls."""

    def test_empty_path(self):
        """Empty string should return False."""
        result = asyncio.get_event_loop().run_until_complete(
            validate_cookies("")
        )
        assert result is False

    def test_nonexistent_path(self):
        """Path that doesn't exist should return False."""
        result = asyncio.get_event_loop().run_until_complete(
            validate_cookies("/tmp/nonexistent_cookie_12345.txt")
        )
        assert result is False
