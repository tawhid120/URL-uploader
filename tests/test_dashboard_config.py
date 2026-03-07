"""Tests for bot.config – new dashboard fields."""

from bot.config import DASHBOARD_PORT, DASHBOARD_TOKEN


class TestDashboardConfig:
    def test_dashboard_port_is_int(self):
        assert isinstance(DASHBOARD_PORT, int)

    def test_dashboard_port_default(self):
        # Default value from env (or 8080 when unset)
        assert DASHBOARD_PORT > 0

    def test_dashboard_token_is_string(self):
        assert isinstance(DASHBOARD_TOKEN, str)
