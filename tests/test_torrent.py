"""Tests for bot.helpers.torrent module."""

from bot.helpers.torrent import is_torrent_or_magnet


class TestIsTorrentOrMagnet:
    def test_magnet_link(self):
        url = "magnet:?xt=urn:btih:abc123&dn=test"
        assert is_torrent_or_magnet(url) is True

    def test_torrent_url(self):
        url = "https://example.com/file.torrent"
        assert is_torrent_or_magnet(url) is True

    def test_torrent_url_with_query(self):
        url = "https://example.com/file.torrent?key=value"
        assert is_torrent_or_magnet(url) is True

    def test_regular_url(self):
        url = "https://www.youtube.com/watch?v=abc"
        assert is_torrent_or_magnet(url) is False

    def test_empty_string(self):
        assert is_torrent_or_magnet("") is False

    def test_magnet_case_insensitive(self):
        url = "MAGNET:?xt=urn:btih:abc"
        assert is_torrent_or_magnet(url) is True
