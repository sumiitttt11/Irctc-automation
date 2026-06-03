"""
poller.py — event-based polling helpers.
All sleeps here are intentional minimum intervals, not dead waits.
"""
import asyncio
from core.logger import log


async def wait_for_element(tab, selector, timeout=15, poll=0.15):
    """Poll until selector appears in DOM, then return it."""
    elapsed = 0.0
    while elapsed < timeout:
        try:
            el = await tab.select(selector)
            if el:
                return el
        except Exception:
            pass
        await asyncio.sleep(poll)
        elapsed += poll
    raise TimeoutError(f"Element not found within {timeout}s: {selector}")


async def wait_for_elements(tab, selector, min_count=1, timeout=15, poll=0.15):
    """Poll until at least min_count elements matching selector exist."""
    elapsed = 0.0
    while elapsed < timeout:
        try:
            els = await tab.select_all(selector)
            if els and len(els) >= min_count:
                return els
        except Exception:
            pass
        await asyncio.sleep(poll)
        elapsed += poll
    raise TimeoutError(f"Expected {min_count}x '{selector}' within {timeout}s")


async def wait_for_js(tab, js_expr, timeout=15, poll=0.15):
    """Poll until JS expression returns truthy."""
    elapsed = 0.0
    while elapsed < timeout:
        try:
            result = await tab.evaluate(js_expr)
            if result:
                return result
        except Exception:
            pass
        await asyncio.sleep(poll)
        elapsed += poll
    raise TimeoutError(f"JS never became truthy within {timeout}s")


async def wait_for_url_contains(tab, substr, timeout=15, poll=0.3):
    """Poll until current URL contains substr."""
    elapsed = 0.0
    while elapsed < timeout:
        try:
            url = await tab.evaluate("window.location.href")
            if substr in url:
                return url
        except Exception:
            pass
        await asyncio.sleep(poll)
        elapsed += poll
    raise TimeoutError(f"URL never contained '{substr}' within {timeout}s")


async def wait_for_element_count_change(tab, selector, prev_count: int, timeout=10, poll=0.15):
    """Poll until the number of matching elements changes from prev_count."""
    elapsed = 0.0
    while elapsed < timeout:
        try:
            els = await tab.select_all(selector)
            if len(els) != prev_count:
                return els
        except Exception:
            pass
        await asyncio.sleep(poll)
        elapsed += poll
    raise TimeoutError(
        f"Element count for '{selector}' did not change from {prev_count} within {timeout}s"
    )
