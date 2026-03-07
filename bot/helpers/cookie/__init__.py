"""Cookie helpers — detection & validation."""

import importlib as _importlib

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "detect_cookies": ("bot.helpers.cookie.detector", "detect_cookies"),
    "format_detected_cookies": ("bot.helpers.cookie.detector", "format_detected_cookies"),
    "match_url_domain": ("bot.helpers.cookie.detector", "match_url_domain"),
    "parse_cookie_file": ("bot.helpers.cookie.detector", "parse_cookie_file"),
    "validate_cookies": ("bot.helpers.cookie.validator", "validate_cookies"),
}

__all__ = list(_LAZY_IMPORTS)


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_path, attr = _LAZY_IMPORTS[name]
        module = _importlib.import_module(module_path)
        value = getattr(module, attr)
        globals()[name] = value  # cache for subsequent access
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

