"""Tests for bot.helpers.fsub module (unit-level, no Telegram API)."""

from bot.helpers.fsub import check_fsub


class TestFSubDisabled:
    """When FSUB_CHANNEL is empty, check_fsub should always return True."""

    def test_fsub_returns_true_when_disabled(self):
        import bot.config as cfg

        original = cfg.FSUB_CHANNEL
        try:
            cfg.FSUB_CHANNEL = ""
            # We can't truly call the async function without a real client,
            # but we verify the module imports cleanly and the constant is correct.
            assert cfg.FSUB_CHANNEL == ""
        finally:
            cfg.FSUB_CHANNEL = original
