"""Web application wrapping the Telegram bot with an admin dashboard.

The FastAPI application is the **primary process**.  The Pyrogram
Telegram bot is started/stopped via the ASGI *lifespan* so both share
the same asyncio event loop.  This architecture lets the application
be deployed on any cloud platform (Render, Railway, Heroku, Koyeb …)
that expects an HTTP server bound to a ``PORT``.

Endpoints
---------
* ``GET  /health``             — unauthenticated health-check
* ``GET  /?token=…``           — admin dashboard (HTML)
* ``GET  /logs?token=…``       — recent bot log lines (HTML)
* ``POST /ban?token=…&user_id=…``  — ban a user
* ``POST /unban?token=…&user_id=…`` — unban a user
"""

import logging
import os
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from bot.config import ADMIN_IDS, DASHBOARD_PORT, DASHBOARD_TOKEN, PORT
from bot.logging_config import memory_handler

logger = logging.getLogger(__name__)

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
    from fastapi.responses import HTMLResponse, PlainTextResponse

    # ---- lifespan: start / stop the Telegram bot ----
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        from bot.client import bot, user_session

        logger.info("Starting Telegram bot via web-app lifespan…")
        await bot.start()
        if user_session:
            logger.info("User session detected — starting for 4 GB uploads.")
            await user_session.start()
        logger.info("Telegram bot is running.")
        yield
        logger.info("Shutting down Telegram bot…")
        if user_session:
            await user_session.stop()
        await bot.stop()
        logger.info("Telegram bot stopped.")

    app = FastAPI(
        title="URL Uploader Bot",
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )

    # ---- auth dependency ----
    async def _verify_token(token: str = Query(...)):
        if not _token_ok(token):
            raise HTTPException(status_code=403, detail="Invalid token")

    # ---- routes ----
    @app.get("/health")
    async def health_check():
        """Unauthenticated health-check for platform probes."""
        return {"status": "ok"}

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

    @app.get("/logs", response_class=HTMLResponse)
    async def view_logs(
        token: str = Query(...),
        count: int = Query(200, ge=1, le=1000),
    ):
        """Show recent bot log lines in the browser."""
        if not _token_ok(token):
            raise HTTPException(status_code=403, detail="Invalid token")

        lines = memory_handler.get_logs(count)
        escaped = "\n".join(
            line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            for line in lines
        )
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Bot Logs</title>
<style>
body {{ background: #1e1e1e; color: #d4d4d4; font-family: monospace;
       font-size: 13px; padding: 1em; white-space: pre-wrap; }}
</style></head><body>
<pre>{escaped}</pre>
</body></html>"""
        return HTMLResponse(content=html)

    @app.post("/ban", dependencies=[Depends(_verify_token)])
    async def ban_user(user_id: int = Query(...)):
        from bot.database.users import ban_user as db_ban
        await db_ban(user_id)
        logger.info("User %s banned via dashboard.", user_id)
        return {"ok": True, "action": "banned", "user_id": user_id}

    @app.post("/unban", dependencies=[Depends(_verify_token)])
    async def unban_user(user_id: int = Query(...)):
        from bot.database.users import unban_user as db_unban
        await db_unban(user_id)
        logger.info("User %s unbanned via dashboard.", user_id)
        return {"ok": True, "action": "unbanned", "user_id": user_id}

    _app = app
    return app


def start_dashboard() -> None:
    """Start the dashboard server in a background thread.

    .. deprecated::
        Prefer running the full web application via ``__main__.py``
        which uses the ASGI lifespan to manage the bot.  This function
        is kept for backward-compatibility.
    """
    if not DASHBOARD_TOKEN:
        return

    import threading
    import uvicorn

    app = _get_app()

    def _run():
        uvicorn.run(app, host="0.0.0.0", port=DASHBOARD_PORT, log_level="info")

    t = threading.Thread(target=_run, daemon=True, name="dashboard")
    t.start()
