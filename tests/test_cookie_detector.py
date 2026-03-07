"""Tests for bot.helpers.cookie_detector module."""

from bot.helpers.cookie.detector import (
    parse_cookie_file,
    detect_cookies,
    format_detected_cookies,
    match_url_domain,
)


# ---- Sample Netscape cookie content ----

_YOUTUBE_COOKIE = """\
# Netscape HTTP Cookie File
# https://curl.haxx.se/docs/http-cookies.html
.youtube.com\tTRUE\t/\tTRUE\t1700000000\tSID\tabc123
.google.com\tTRUE\t/\tTRUE\t1700000000\tHSID\txyz789
"""

_MULTI_SITE_COOKIE = """\
# Netscape HTTP Cookie File
.youtube.com\tTRUE\t/\tTRUE\t0\tPREF\tf1
.instagram.com\tTRUE\t/\tTRUE\t0\tds_user_id\t123
.twitter.com\tTRUE\t/\tTRUE\t0\tauth_token\ttt
.x.com\tTRUE\t/\tTRUE\t0\tauth_token\ttt2
.reddit.com\tTRUE\t/\tTRUE\t0\ttoken_v2\trr
"""

_EMPTY_COOKIE = """\
# Netscape HTTP Cookie File
# This file has no actual cookie entries
"""

_SUBDOMAIN_COOKIE = """\
# Netscape HTTP Cookie File
.accounts.google.com\tTRUE\t/\tTRUE\t0\tGAPISID\tabc
.www.youtube.com\tTRUE\t/\tTRUE\t0\tVISITOR\txyz
.m.facebook.com\tTRUE\t/\tTRUE\t0\tc_user\t111
"""


class TestParseCookieFile:
    """Tests for parse_cookie_file()."""

    def test_youtube_google_cookies(self):
        domains = parse_cookie_file(_YOUTUBE_COOKIE)
        assert "youtube.com" in domains
        assert "google.com" in domains

    def test_multi_site_returns_sorted_unique(self):
        domains = parse_cookie_file(_MULTI_SITE_COOKIE)
        assert domains == sorted(domains)
        assert "youtube.com" in domains
        assert "instagram.com" in domains
        assert "twitter.com" in domains
        assert "x.com" in domains
        assert "reddit.com" in domains

    def test_empty_cookie_file(self):
        domains = parse_cookie_file(_EMPTY_COOKIE)
        assert domains == []

    def test_blank_string(self):
        domains = parse_cookie_file("")
        assert domains == []

    def test_subdomain_extraction(self):
        """Subdomains like .accounts.google.com should resolve to google.com."""
        domains = parse_cookie_file(_SUBDOMAIN_COOKIE)
        assert "google.com" in domains
        assert "youtube.com" in domains
        assert "facebook.com" in domains
        # There shouldn't be full subdomains
        assert "accounts.google.com" not in domains

    def test_ignores_comments(self):
        text = "# Comment line\n# Another comment\n"
        assert parse_cookie_file(text) == []

    def test_ignores_malformed_lines(self):
        text = "only\ttwo\tfields\n"
        assert parse_cookie_file(text) == []

    def test_country_code_tld(self):
        """Domains like .bbc.co.uk should resolve correctly."""
        text = ".bbc.co.uk\tTRUE\t/\tTRUE\t0\tck\tval\n"
        domains = parse_cookie_file(text)
        assert "bbc.co.uk" in domains
        assert "co.uk" not in domains


class TestDetectCookies:
    """Tests for detect_cookies()."""

    def test_returns_domains_and_labels(self):
        result = detect_cookies(_YOUTUBE_COOKIE)
        assert "domains" in result
        assert "labels" in result
        assert len(result["domains"]) == len(result["labels"])

    def test_friendly_labels(self):
        result = detect_cookies(_YOUTUBE_COOKIE)
        assert "🎬 YouTube" in result["labels"]
        assert "🔍 Google" in result["labels"]

    def test_multi_site_labels(self):
        result = detect_cookies(_MULTI_SITE_COOKIE)
        assert "📸 Instagram" in result["labels"]
        assert "🐦 Twitter / X" in result["labels"]
        assert "🤖 Reddit" in result["labels"]

    def test_unknown_domain_gets_globe_emoji(self):
        text = ".example.org\tTRUE\t/\tTRUE\t0\tkey\tval\n"
        result = detect_cookies(text)
        assert "🌐 example.org" in result["labels"]

    def test_empty_file(self):
        result = detect_cookies("")
        assert result["domains"] == []
        assert result["labels"] == []


class TestFormatDetectedCookies:
    """Tests for format_detected_cookies()."""

    def test_formats_detected(self):
        detection = detect_cookies(_YOUTUBE_COOKIE)
        msg = format_detected_cookies(detection)
        assert "Smart Cookie Detector" in msg
        assert "YouTube" in msg
        assert "Google" in msg
        assert "2" in msg  # 2 sites

    def test_empty_detection(self):
        detection = {"domains": [], "labels": []}
        msg = format_detected_cookies(detection)
        assert "No website cookies detected" in msg


class TestMatchUrlDomain:
    """Tests for match_url_domain()."""

    def test_youtube_url_matches(self):
        domains = ["youtube.com", "google.com"]
        assert match_url_domain("https://www.youtube.com/watch?v=abc", domains) is True

    def test_instagram_url_matches(self):
        domains = ["instagram.com"]
        assert match_url_domain("https://www.instagram.com/reel/abc", domains) is True

    def test_unrelated_url_no_match(self):
        domains = ["youtube.com"]
        assert match_url_domain("https://www.instagram.com/p/abc", domains) is False

    def test_empty_domains(self):
        assert match_url_domain("https://www.youtube.com/watch?v=x", []) is False

    def test_invalid_url(self):
        assert match_url_domain("not a url", ["youtube.com"]) is False

    def test_empty_url(self):
        assert match_url_domain("", ["youtube.com"]) is False
