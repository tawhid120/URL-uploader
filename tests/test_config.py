"""Tests for bot.config module."""

from bot.config import PLAN_LIMITS, DOWNLOAD_DIR


class TestPlanLimits:
    def test_free_limits(self):
        free = PLAN_LIMITS["free"]
        assert free["files"] == 10
        assert free["bandwidth"] == 2 * 1024**3

    def test_basic_limits(self):
        basic = PLAN_LIMITS["basic"]
        assert basic["files"] == 50
        assert basic["bandwidth"] == 10 * 1024**3

    def test_standard_limits(self):
        standard = PLAN_LIMITS["standard"]
        assert standard["files"] == 100
        assert standard["bandwidth"] == 30 * 1024**3

    def test_pro_limits(self):
        pro = PLAN_LIMITS["pro"]
        assert pro["files"] == float("inf")
        assert pro["bandwidth"] == float("inf")


class TestDownloadDir:
    def test_download_dir_set(self):
        assert DOWNLOAD_DIR is not None
        assert isinstance(DOWNLOAD_DIR, str)
        assert len(DOWNLOAD_DIR) > 0
