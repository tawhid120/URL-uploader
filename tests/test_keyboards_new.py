"""Tests for bot.helpers.keyboards — new caption buttons in settings_keyboard."""

from bot.helpers.keyboards import settings_keyboard


class TestSettingsKeyboardCaption:
    def test_has_caption_buttons(self):
        kb = settings_keyboard()
        callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
        assert "set_caption" in callbacks
        assert "del_caption" in callbacks

    def test_has_all_expected_buttons(self):
        kb = settings_keyboard()
        callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
        expected = {
            "set_thumb", "del_thumb", "set_caption", "del_caption",
            "manage_cookies", "show_upgrade", "refresh_settings",
        }
        assert expected.issubset(set(callbacks))
