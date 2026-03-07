"""Lightweight admin web dashboard using FastAPI.

Provides a read-only overview of bot statistics and user management
(ban / unban).  Guarded by a simple token-based authentication.
"""

import os
import secrets
from datetime import datetime, timezone

from bot.config import ADMIN_IDS, DASHBOARD_PORT, DASHBOARD_TOKEN

# Lazy imports – FastAPI / uvicorn are optional dependencies.
_app = None


def _token_ok(token: str) -> bool:
    """Constant-time comparison of *token* against the configured secret."""
    if not DASHBOARD_TOKEN:
        return False
    return secrets.compare_digest(token, DASHBOARD_TOKEN)


def _get_app():
    """Return the shared FastAPI application (created on first call)."""
    global _app
    if _app is not None:
        return _app

    from fastapi import FastAPI, Depends, HTTPException, Query
    from fastapi.responses import HTMLResponse

    app = FastAPI(title="URL Uploader Dashboard", docs_url=None, redoc_url=None)

    # ---- auth dependency ----
    async def _verify_token(token: str = Query(...)):
        if not _token_ok(token):
            raise HTTPException(status_code=403, detail="Invalid token")

    # ---- routes ----
    @app.get("/", response_class=HTMLResponse)
    async def dashboard(token: str = Query(...)):
        """Main dashboard page."""
        if not _token_ok(token):
            raise HTTPException(status_code=403, detail="Invalid token")

        from bot.database.users import users_col

        total_users = await users_col.count_documents({})
        banned_users = await users_col.count_documents({"banned": True})

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        pipeline = [
            {"$match": {"daily.date": today}},
            {
                "$group": {
                    "_id": None,
                    "total_files": {"$sum": "$daily.files"},
                    "total_bandwidth": {"$sum": "$daily.bandwidth"},
                }
            },
        ]
        cursor = users_col.aggregate(pipeline)
        stats = await cursor.to_list(length=1)
        daily_files = stats[0]["total_files"] if stats else 0
        daily_bw = stats[0]["total_bandwidth"] if stats else 0
        daily_bw_gb = round(daily_bw / (1024**3), 2) if daily_bw else 0

        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Bot Dashboard</title>
<style>
body {{ font-family: sans-serif; margin: 2em; background: #f5f5f5; }}
.card {{ background: #fff; border-radius: 10px; padding: 1.5em; margin: 1em 0;
         box-shadow: 0 2px 6px rgba(0,0,0,.1); }}
h1 {{ color: #333; }}
.stat {{ font-size: 2em; font-weight: bold; color: #0088cc; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1em; }}
</style></head><body>
<h1>📊 URL Uploader Bot — Dashboard</h1>
<div class="grid">
  <div class="card"><div class="stat">{total_users}</div>Total Users</div>
  <div class="card"><div class="stat">{banned_users}</div>Banned Users</div>
  <div class="card"><div class="stat">{daily_files}</div>Files Today</div>
  <div class="card"><div class="stat">{daily_bw_gb} GB</div>Bandwidth Today</div>
</div>
</body></html>"""
        return HTMLResponse(content=html)

    @app.post("/ban", dependencies=[Depends(_verify_token)])
    async def ban_user(user_id: int = Query(...)):
        from bot.database.users import ban_user as db_ban
        await db_ban(user_id)
        return {"ok": True, "action": "banned", "user_id": user_id}

    @app.post("/unban", dependencies=[Depends(_verify_token)])
    async def unban_user(user_id: int = Query(...)):
        from bot.database.users import unban_user as db_unban
        await db_unban(user_id)
        return {"ok": True, "action": "unbanned", "user_id": user_id}

    _app = app
    return app


def start_dashboard() -> None:
    """Start the dashboard server in a background thread.

    This is a non-blocking call that spawns a uvicorn server on
    ``DASHBOARD_PORT``.  It does nothing if DASHBOARD_TOKEN is not
    configured.
    """
    if not DASHBOARD_TOKEN:
        return

    import threading
    import uvicorn

    app = _get_app()

    def _run():
        uvicorn.run(app, host="127.0.0.1", port=DASHBOARD_PORT, log_level="warning")

    t = threading.Thread(target=_run, daemon=True, name="dashboard")
    t.start()
