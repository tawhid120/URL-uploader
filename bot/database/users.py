from datetime import datetime, timezone

import motor.motor_asyncio

from bot.config import MONGO_URI, DB_NAME

_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = _client[DB_NAME]
users_col = db["users"]


def _today() -> str:
    """Return today's date as YYYY-MM-DD string (UTC)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


async def ensure_user(user_id: int, first_name: str) -> dict:
    """Create user document if it doesn't exist, then return it."""
    user = await users_col.find_one({"_id": user_id})
    if user is None:
        user = {
            "_id": user_id,
            "first_name": first_name,
            "plan": "free",
            "plan_expiry": None,
            "joined": datetime.now(timezone.utc),
            "thumbnail": None,
            "cookie_file_id": None,
            "caption": None,
            "banned": False,
            "daily": {
                "date": _today(),
                "files": 0,
                "bandwidth": 0,
            },
        }
        await users_col.insert_one(user)
    return user


async def get_user(user_id: int) -> dict | None:
    """Fetch a user document."""
    return await users_col.find_one({"_id": user_id})


async def _reset_daily_if_needed(user_id: int, user: dict) -> dict:
    """Reset daily counters if the date has changed."""
    if user.get("daily", {}).get("date") != _today():
        await users_col.update_one(
            {"_id": user_id},
            {"$set": {"daily": {"date": _today(), "files": 0, "bandwidth": 0}}},
        )
        user["daily"] = {"date": _today(), "files": 0, "bandwidth": 0}
    return user


async def get_daily_usage(user_id: int) -> dict:
    """Return daily usage after resetting if needed."""
    user = await get_user(user_id)
    if user is None:
        return {"date": _today(), "files": 0, "bandwidth": 0}
    user = await _reset_daily_if_needed(user_id, user)
    return user["daily"]


async def increment_usage(user_id: int, file_size: int) -> None:
    """Increment the file count and bandwidth for today."""
    user = await get_user(user_id)
    if user is None:
        return
    await _reset_daily_if_needed(user_id, user)
    await users_col.update_one(
        {"_id": user_id},
        {"$inc": {"daily.files": 1, "daily.bandwidth": file_size}},
    )


async def set_plan(user_id: int, plan: str, expiry: datetime | None = None) -> None:
    """Update a user's subscription plan."""
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"plan": plan, "plan_expiry": expiry}},
    )


async def set_thumbnail(user_id: int, file_id: str | None) -> None:
    """Set or clear a user's custom thumbnail."""
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"thumbnail": file_id}},
    )


async def set_cookie(user_id: int, file_id: str | None) -> None:
    """Set or clear a user's cookie file_id."""
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"cookie_file_id": file_id}},
    )


async def set_caption(user_id: int, caption: str | None) -> None:
    """Set or clear a user's custom caption template."""
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"caption": caption}},
    )


async def ban_user(user_id: int) -> None:
    """Ban a user from using the bot."""
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"banned": True}},
    )


async def unban_user(user_id: int) -> None:
    """Un-ban a user."""
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"banned": False}},
    )


async def is_banned(user_id: int) -> bool:
    """Check if a user is banned."""
    user = await get_user(user_id)
    if user is None:
        return False
    return bool(user.get("banned", False))


async def get_all_user_ids() -> list[int]:
    """Return a list of all user IDs in the database."""
    cursor = users_col.find({}, {"_id": 1})
    return [doc["_id"] async for doc in cursor]
