"""Tests for the web application layer (bot.dashboard)."""

import pytest

from bot.config import PORT, DASHBOARD_PORT


class TestPortConfig:
    def test_port_is_int(self):
        assert isinstance(PORT, int)

    def test_port_positive(self):
        assert PORT > 0

    def test_port_defaults_to_dashboard_port(self):
        # When PORT env var is not set, it falls back to DASHBOARD_PORT
        import os
        if "PORT" not in os.environ:
            assert PORT == DASHBOARD_PORT


class TestDashboardApp:
    def test_get_app_returns_fastapi(self):
        from bot.dashboard import _get_app
        app = _get_app()
        # FastAPI is a subclass of Starlette which has .routes
        assert hasattr(app, "routes")

    def test_health_route_exists(self):
        from bot.dashboard import _get_app
        app = _get_app()
        route_paths = [r.path for r in app.routes if hasattr(r, "path")]
        assert "/health" in route_paths

    def test_logs_route_exists(self):
        from bot.dashboard import _get_app
        app = _get_app()
        route_paths = [r.path for r in app.routes if hasattr(r, "path")]
        assert "/logs" in route_paths

    def test_root_route_exists(self):
        from bot.dashboard import _get_app
        app = _get_app()
        route_paths = [r.path for r in app.routes if hasattr(r, "path")]
        assert "/" in route_paths
