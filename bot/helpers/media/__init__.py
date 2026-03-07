"""Media processing helpers — split, thumbnail & zip."""

import importlib as _importlib

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "split_file": ("bot.helpers.media.split", "split_file"),
    "generate_thumbnail": ("bot.helpers.media.thumbnail", "generate_thumbnail"),
    "create_zip": ("bot.helpers.media.zipper", "create_zip"),
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

