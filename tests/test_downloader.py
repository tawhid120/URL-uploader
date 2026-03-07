"""Tests for bot.helpers.downloader module (build_format_list only, no network)."""

from bot.helpers.download import build_format_list


class TestBuildFormatList:
    def test_empty_info(self):
        assert build_format_list({}) == []

    def test_no_formats_key(self):
        assert build_format_list({"title": "test"}) == []

    def test_filters_by_ext(self):
        formats = [
            {"height": 720, "ext": "mp4", "format_id": "136"},
            {"height": 480, "ext": "3gp", "format_id": "17"},
            {"height": 1080, "ext": "webm", "format_id": "248"},
        ]
        result = build_format_list({"formats": formats})
        exts = [r["label"] for r in result]
        assert all("mp4" in e or "webm" in e for e in exts)
        assert not any("3gp" in e for e in exts)

    def test_sorted_descending(self):
        formats = [
            {"height": 480, "ext": "mp4", "format_id": "135"},
            {"height": 1080, "ext": "mp4", "format_id": "137"},
            {"height": 720, "ext": "mp4", "format_id": "136"},
        ]
        result = build_format_list({"formats": formats})
        heights = [r["height"] for r in result]
        assert heights == sorted(heights, reverse=True)

    def test_skips_no_height(self):
        formats = [
            {"ext": "mp4", "format_id": "audio_only"},
            {"height": 720, "ext": "mp4", "format_id": "136"},
        ]
        result = build_format_list({"formats": formats})
        assert len(result) == 1
        assert result[0]["height"] == 720
