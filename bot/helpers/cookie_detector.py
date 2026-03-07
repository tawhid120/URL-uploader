"""Smart Cookie Auto-Detector.

Parses Netscape-format cookie files, detects which domains/websites
the cookies belong to, and provides human-friendly site labels so the
bot can inform the user exactly what was detected.
"""

from __future__ import annotations

from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Well-known domain → friendly name mapping
# ---------------------------------------------------------------------------
_DOMAIN_LABELS: dict[str, str] = {
    "youtube.com": "🎬 YouTube",
    "youtu.be": "🎬 YouTube",
    "google.com": "🔍 Google",
    "instagram.com": "📸 Instagram",
    "twitter.com": "🐦 Twitter / X",
    "x.com": "🐦 Twitter / X",
    "facebook.com": "📘 Facebook",
    "fb.com": "📘 Facebook",
    "tiktok.com": "🎵 TikTok",
    "reddit.com": "🤖 Reddit",
    "twitch.tv": "🎮 Twitch",
    "vimeo.com": "🎥 Vimeo",
    "dailymotion.com": "📺 Dailymotion",
    "soundcloud.com": "🎧 SoundCloud",
    "bilibili.com": "📺 Bilibili",
    "nicovideo.jp": "📺 Niconico",
    "crunchyroll.com": "🍥 Crunchyroll",
    "netflix.com": "🎬 Netflix",
    "hotstar.com": "⭐ Hotstar",
    "zee5.com": "📺 ZEE5",
    "primevideo.com": "🎬 Prime Video",
    "amazon.com": "🛒 Amazon",
    "pinterest.com": "📌 Pinterest",
    "linkedin.com": "💼 LinkedIn",
    "tumblr.com": "📝 Tumblr",
    "spotify.com": "🎵 Spotify",
    "dropbox.com": "📦 Dropbox",
    "mega.nz": "📦 MEGA",
    "mediafire.com": "📦 MediaFire",
    "drive.google.com": "📁 Google Drive",
}


def _root_domain(domain: str) -> str:
    """Return the registrable (root) domain from a cookie domain string.

    Cookie domains may start with a leading dot (e.g. ``.youtube.com``).
    This helper strips that prefix and returns the last two labels
    (or the full domain when it has only two labels).

    >>> _root_domain(".accounts.google.com")
    'google.com'
    >>> _root_domain("youtu.be")
    'youtu.be'
    """
    domain = domain.lstrip(".").lower().strip()
    parts = domain.split(".")
    if len(parts) > 2:
        return ".".join(parts[-2:])
    return domain


def _friendly_name(domain: str) -> str:
    """Map a root domain to a human-friendly label.

    Falls back to the domain itself when no mapping is found.
    """
    return _DOMAIN_LABELS.get(domain, f"🌐 {domain}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_cookie_file(text: str) -> list[str]:
    """Parse Netscape cookie file content and return unique root domains.

    Each non-comment, non-blank line in a Netscape cookie file has the
    format::

        <domain>  <flag>  <path>  <secure>  <expiry>  <name>  <value>

    Fields are separated by one or more TAB characters.

    Returns a **sorted** list of unique root domains found in the file.
    """
    domains: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        # Skip blank lines, comments, and the magic header
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 7:
            root = _root_domain(parts[0])
            if root:
                domains.add(root)
    return sorted(domains)


def detect_cookies(text: str) -> dict[str, list[str]]:
    """High-level detector: parse a Netscape cookie file and return results.

    Returns a dict with:
    * ``"domains"`` – sorted list of root domains found.
    * ``"labels"``  – matching list of friendly website labels.
    """
    domains = parse_cookie_file(text)
    labels = [_friendly_name(d) for d in domains]
    return {"domains": domains, "labels": labels}


def format_detected_cookies(detection: dict[str, list[str]]) -> str:
    """Format detection results into a user-facing message."""
    labels = detection.get("labels", [])
    if not labels:
        return "⚠️ No website cookies detected in this file."
    header = f"🍪 **Smart Cookie Detector** — Found cookies for **{len(labels)}** site(s):\n\n"
    body = "\n".join(f"  • {label}" for label in labels)
    footer = "\n\n✅ These cookies will be used automatically when you download from the detected sites."
    return header + body + footer


def match_url_domain(url: str, cookie_domains: list[str]) -> bool:
    """Return ``True`` if *url* belongs to one of the *cookie_domains*.

    Useful for informing the user whether their stored cookie covers the
    URL they are trying to download from.
    """
    try:
        hostname = urlparse(url).hostname or ""
    except Exception:
        return False
    url_root = _root_domain(hostname)
    return url_root in cookie_domains
