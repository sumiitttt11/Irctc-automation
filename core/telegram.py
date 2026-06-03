"""
telegram.py — Telegram Bot notification helper.

Set in .env:
    TELEGRAM_BOT_TOKEN=<your token>
    TELEGRAM_CHAT_ID=<your chat id>

If either is missing, notifications are silently skipped.
Get a token: BotFather (@BotFather on Telegram) → /newbot
Get your chat id: message @userinfobot
"""
import os
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from core.logger import log

load_dotenv()

_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")
_ENABLED   = bool(_BOT_TOKEN and _CHAT_ID)


async def _send(text: str, photo_path: str | None = None) -> None:
    """Low-level sender. Uses aiohttp if available, else urllib."""
    if not _ENABLED:
        return
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            if photo_path and Path(photo_path).exists():
                url = f"https://api.telegram.org/bot{_BOT_TOKEN}/sendPhoto"
                with open(photo_path, "rb") as f:
                    form = aiohttp.FormData()
                    form.add_field("chat_id", _CHAT_ID)
                    form.add_field("caption", text[:1024])
                    form.add_field("photo", f, filename="screenshot.png")
                    await session.post(url, data=form)
            else:
                url = f"https://api.telegram.org/bot{_BOT_TOKEN}/sendMessage"
                await session.post(url, json={
                    "chat_id": _CHAT_ID,
                    "text": text,
                    "parse_mode": "HTML"
                })
    except ImportError:
        # Fallback: urllib (stdlib)
        import urllib.request, urllib.parse
        url = f"https://api.telegram.org/bot{_BOT_TOKEN}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": _CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }).encode()
        urllib.request.urlopen(url, payload, timeout=10)


async def notify_success(pnr: str, train: str, travel_class: str,
                          passengers: list[str]) -> None:
    pax = "\n".join(f"  • {p}" for p in passengers)
    msg = (
        f"✅ <b>BOOKING CONFIRMED</b>\n\n"
        f"🚆 Train: <b>{train}</b>\n"
        f"🪑 Class: <b>{travel_class}</b>\n"
        f"🔖 PNR:   <code>{pnr}</code>\n\n"
        f"<b>Passengers:</b>\n{pax}"
    )
    log.info(f"📲 Telegram: booking success — PNR {pnr}")
    await _send(msg)


async def notify_failure(error: str, screenshot_path: str | None = None) -> None:
    msg = (
        f"❌ <b>BOOKING FAILED</b>\n\n"
        f"<pre>{error[:800]}</pre>"
    )
    log.info("📲 Telegram: booking failure notification")
    await _send(msg, photo_path=screenshot_path)


async def notify_captcha_needed() -> None:
    msg = "🤖 <b>CAPTCHA required</b> — please solve it manually in the browser window."
    await _send(msg)


async def notify_fire_imminent(seconds_left: float) -> None:
    msg = f"⏰ <b>Fire time in {seconds_left:.0f}s</b> — stand by…"
    await _send(msg)
