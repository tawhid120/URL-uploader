import humanize


def human_bytes(size: int | float) -> str:
    """Convert bytes to a human-readable string (e.g. '1.95 GB')."""
    if size == float("inf"):
        return "Unlimited"
    return humanize.naturalsize(size, binary=False, format="%.2f")


def plan_display(plan: str) -> str:
    """Return emoji + label for a plan name."""
    mapping = {
        "free": "🆓 Free",
        "basic": "⭐ Basic",
        "standard": "🔷 Standard",
        "pro": "💎 Pro",
    }
    return mapping.get(plan, plan)
