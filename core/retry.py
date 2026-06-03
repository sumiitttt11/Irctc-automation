"""
retry.py — retry decorator with exponential back-off + screenshot on crash.

Usage:
    @retryable(retries=3, delay=1.0)
    async def my_func(tab, ...):
        ...

On every failed attempt the decorator:
  1. Logs the error with attempt number
  2. Takes a screenshot to storage/screenshots/
  3. Waits delay * 2^attempt seconds before next try
  4. Raises the last exception if all attempts exhausted
"""
import asyncio
import functools
import time
from pathlib import Path

from core.logger import log

SCREENSHOT_DIR = Path("storage/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


async def _take_screenshot(tab, label: str):
    try:
        ts = int(time.time())
        path = SCREENSHOT_DIR / f"{label}_{ts}.png"
        await tab.save_screenshot(str(path))
        log.info(f"📸 Screenshot saved: {path}")
    except Exception as e:
        log.warning(f"Screenshot failed: {e}")


def retryable(retries: int = 3, delay: float = 1.0, screenshot: bool = True):
    """
    Decorator for async functions whose first positional arg after self/tab is `tab`.
    Retries on any exception up to `retries` times with exponential back-off.
    """
    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            # Try to find a `tab` argument for screenshots
            tab = None
            if args:
                # Convention: tab is the first arg (or second if method)
                for a in args:
                    if hasattr(a, "evaluate"):   # duck-type nodriver tab
                        tab = a
                        break

            last_exc = None
            for attempt in range(1, retries + 1):
                try:
                    return await fn(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    log.warning(
                        f"⚠ {fn.__name__} attempt {attempt}/{retries} failed: {exc}"
                    )
                    if screenshot and tab:
                        await _take_screenshot(tab, f"crash_{fn.__name__}_attempt{attempt}")
                    if attempt < retries:
                        wait = delay * (2 ** (attempt - 1))
                        log.info(f"↻ Retrying in {wait:.1f}s …")
                        await asyncio.sleep(wait)

            log.error(f"❌ {fn.__name__} failed after {retries} attempts")
            raise last_exc

        return wrapper
    return decorator
