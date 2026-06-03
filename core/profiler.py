"""
profiler.py — lightweight timing profiler.

Usage (context manager):
    async with timed("login"):
        await fill_login(tab)

Usage (decorator):
    @profile
    async def fill_passengers(tab, data): ...

All timings are accumulated and printed in a summary table at the end.
"""
import time
import asyncio
import functools
from contextlib import asynccontextmanager
from core.logger import log

_timings: list[tuple[str, float]] = []


@asynccontextmanager
async def timed(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        _timings.append((label, elapsed))
        log.debug(f"⏱  {label}: {elapsed*1000:.0f} ms")


def profile(fn):
    """Decorator version — wraps the whole async function."""
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        async with timed(fn.__name__):
            return await fn(*args, **kwargs)
    return wrapper


def print_summary():
    if not _timings:
        return
    total = sum(t for _, t in _timings)
    print("\n" + "═" * 50)
    print("  TIMING SUMMARY")
    print("═" * 50)
    for label, t in _timings:
        bar = "█" * int(t / total * 30)
        print(f"  {label:<28} {t*1000:>7.0f} ms  {bar}")
    print("─" * 50)
    print(f"  {'TOTAL':<28} {total*1000:>7.0f} ms")
    print("═" * 50 + "\n")
