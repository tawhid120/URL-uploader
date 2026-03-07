"""Tests for bot.helpers.utils module."""

import math

from bot.helpers.utils import human_bytes, plan_display


class TestHumanBytes:
    def test_zero(self):
        result = human_bytes(0)
        assert "0" in result

    def test_megabytes(self):
        result = human_bytes(1_000_000)
        assert "MB" in result or "M" in result

    def test_gigabytes(self):
        result = human_bytes(2 * 1024**3)
        assert "G" in result

    def test_infinity(self):
        assert human_bytes(float("inf")) == "Unlimited"


class TestPlanDisplay:
    def test_free(self):
        assert plan_display("free") == "🆓 Free"

    def test_basic(self):
        assert plan_display("basic") == "⭐ Basic"

    def test_standard(self):
        assert plan_display("standard") == "🔷 Standard"

    def test_pro(self):
        assert plan_display("pro") == "💎 Pro"

    def test_unknown_plan(self):
        assert plan_display("unknown") == "unknown"
