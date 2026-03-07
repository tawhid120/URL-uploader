"""Tests for new config additions."""

from bot.config import (
    ADMIN_IDS,
    SESSION_STR,
    FSUB_CHANNEL,
    TG_BOT_FILE_LIMIT,
    TG_USER_FILE_LIMIT,
    TG_SPLIT_SIZE,
)


class TestNewConfigFields:
    def test_admin_ids_is_list(self):
        assert isinstance(ADMIN_IDS, list)

    def test_session_str_is_string(self):
        assert isinstance(SESSION_STR, str)

    def test_fsub_channel_is_string(self):
        assert isinstance(FSUB_CHANNEL, str)

    def test_tg_bot_file_limit(self):
        assert TG_BOT_FILE_LIMIT == 2 * 1024**3

    def test_tg_user_file_limit(self):
        assert TG_USER_FILE_LIMIT == 4 * 1024**3

    def test_tg_split_size(self):
        assert TG_SPLIT_SIZE < TG_BOT_FILE_LIMIT
        assert TG_SPLIT_SIZE > 0
