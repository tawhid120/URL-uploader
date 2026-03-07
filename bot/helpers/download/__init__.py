"""Download helpers — yt-dlp, torrent & playlist."""

import importlib as _importlib

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "build_format_list": ("bot.helpers.download.downloader", "build_format_list"),
    "download_media": ("bot.helpers.download.downloader", "download_media"),
    "extract_info": ("bot.helpers.download.downloader", "extract_info"),
    "download_playlist": ("bot.helpers.download.playlist", "download_playlist"),
    "is_playlist_url": ("bot.helpers.download.playlist", "is_playlist_url"),
    "download_torrent": ("bot.helpers.download.torrent", "download_torrent"),
    "is_torrent_or_magnet": ("bot.helpers.download.torrent", "is_torrent_or_magnet"),
}

__all__ = list(_LAZY_IMPORTS)


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_path, attr = _LAZY_IMPORTS[name]
        module = _importlib.import_module(module_path)
        value = getattr(module, attr)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

