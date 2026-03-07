"""Tests for bot.helpers.keyboards module."""

from bot.helpers.keyboards import (
    settings_keyboard,
    cookie_keyboard,
    upgrade_keyboard,
    quality_keyboard,
)


class TestSettingsKeyboard:
    def test_returns_markup(self):
        kb = settings_keyboard()
        assert kb is not None
        assert hasattr(kb, "inline_keyboard")
        assert len(kb.inline_keyboard) > 0

    def test_has_upgrade_button(self):
        kb = settings_keyboard()
        texts = [btn.text for row in kb.inline_keyboard for btn in row]
        assert any("Upgrade" in t for t in texts)


class TestCookieKeyboard:
    def test_returns_markup(self):
        kb = cookie_keyboard()
        assert kb is not None
        assert len(kb.inline_keyboard) > 0

    def test_has_upload_button(self):
        kb = cookie_keyboard()
        texts = [btn.text for row in kb.inline_keyboard for btn in row]
        assert any("Upload" in t for t in texts)


class TestUpgradeKeyboard:
    def test_returns_markup(self):
        kb = upgrade_keyboard()
        assert kb is not None
        assert len(kb.inline_keyboard) > 0

    def test_has_plan_buttons(self):
        kb = upgrade_keyboard()
        callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
        assert "plan_basic" in callbacks
        assert "plan_standard" in callbacks
        assert "plan_pro" in callbacks


class TestQualityKeyboard:
    def test_empty_formats(self):
        kb = quality_keyboard([])
        # Should only have the "Audio Only" button
        assert len(kb.inline_keyboard) == 1
        assert kb.inline_keyboard[0][0].callback_data == "fmt|audio"

    def test_with_formats(self):
        formats = [
            {"label": "1080p — mp4", "format_id": "137"},
            {"label": "720p — mp4", "format_id": "136"},
        ]
        kb = quality_keyboard(formats)
        # 2 format buttons + 1 audio button
        assert len(kb.inline_keyboard) == 3

    def test_deduplicates_labels(self):
        formats = [
            {"label": "720p — mp4", "format_id": "136"},
            {"label": "720p — mp4", "format_id": "136b"},
        ]
        kb = quality_keyboard(formats)
        # 1 unique format + 1 audio = 2
        assert len(kb.inline_keyboard) == 2
