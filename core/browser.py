"""
browser.py — nodriver browser factory with session / cookie persistence.

Saves cookies to storage/session.json after a successful login.
Loads and injects them on the next run, skipping re-login + CAPTCHA.
Detects session expiry and triggers a fresh login if needed.
"""
import json
import asyncio
from pathlib import Path

import nodriver as uc
from core.logger import log

SESSION_FILE = Path("storage/session.json")
SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)


async def create_browser():
    browser = await uc.start(
        headless=False,
        browser_args=[
            "--start-maximized",
            "--window-size=1920,1080",
        ]
    )
    tab = await browser.get("about:blank")
    log.info("🌐 Browser started")
    return browser, tab


async def save_cookies(tab) -> None:
    """Save all cookies for irctc.co.in to SESSION_FILE."""
    try:
        cookies = await tab.send(uc.cdp.network.get_cookies(
            urls=["https://www.irctc.co.in"]
        ))
        # cookies is a list of Cookie CDP objects; serialise to plain dicts
        data = [
            {
                "name":    c.name,
                "value":   c.value,
                "domain":  c.domain,
                "path":    c.path,
                "expires": c.expires,
                "httpOnly": c.http_only,
                "secure":  c.secure,
            }
            for c in (cookies or [])
        ]
        SESSION_FILE.write_text(json.dumps(data, indent=2))
        log.info(f"💾 Session saved ({len(data)} cookies) → {SESSION_FILE}")
    except Exception as e:
        log.warning(f"Could not save cookies: {e}")


async def load_cookies(tab) -> bool:
    """
    Inject saved cookies into the browser.
    Returns True if cookies were loaded, False if no session file exists.
    """
    if not SESSION_FILE.exists():
        return False
    try:
        data = json.loads(SESSION_FILE.read_text())
        for c in data:
            await tab.send(uc.cdp.network.set_cookie(
                name=c["name"],
                value=c["value"],
                domain=c.get("domain", ".irctc.co.in"),
                path=c.get("path", "/"),
                expires=c.get("expires"),
                http_only=c.get("httpOnly", False),
                secure=c.get("secure", True),
            ))
        log.info(f"🔑 Session loaded ({len(data)} cookies)")
        return True
    except Exception as e:
        log.warning(f"Could not load cookies: {e}")
        return False


async def is_session_valid(tab) -> bool:
    """
    Navigate to IRCTC and check whether we're still logged in.
    A logged-in session shows the user-greeting element.
    """
    try:
        await tab.get("https://www.irctc.co.in/nget/train-search")
        await asyncio.sleep(2)
        result = await tab.evaluate(
            "document.querySelector('.user-name-id, .loginText') !== null"
        )
        return bool(result)
    except Exception:
        return False


def clear_session() -> None:
    """Delete the saved session file (e.g. after a logout or expiry)."""
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
        log.info("🗑  Session file cleared")
