"""Tests for admin utility logic (import-safe, avoids motor dependency)."""

from bot.config import ADMIN_IDS


class TestAdminConfig:
    def test_admin_ids_is_list(self):
        assert isinstance(ADMIN_IDS, list)

    def test_all_admin_ids_are_ints(self):
        for aid in ADMIN_IDS:
            assert isinstance(aid, int)
