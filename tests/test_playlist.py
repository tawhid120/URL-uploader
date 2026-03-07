"""Tests for bot.helpers.playlist module."""

from bot.helpers.playlist import is_playlist_url


class TestIsPlaylistUrl:
    def test_playlist_type(self):
        info = {"_type": "playlist", "entries": []}
        assert is_playlist_url(info) is True

    def test_has_entries(self):
        info = {"entries": [{"title": "Video 1"}]}
        assert is_playlist_url(info) is True

    def test_single_video(self):
        info = {"title": "Single video", "formats": []}
        assert is_playlist_url(info) is False

    def test_empty_dict(self):
        assert is_playlist_url({}) is False
