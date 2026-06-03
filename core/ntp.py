"""
ntp.py — NTP clock offset calculation.

Queries pool.ntp.org on startup and computes the offset between
local system time and true network time. The offset is used in
the fire-time loop so a clock that's 3 s behind doesn't cost you
the booking window.
"""
import time
from core.logger import log

_offset: float = 0.0   # seconds (positive = local clock is behind)


def sync_clock() -> float:
    """
    Attempt NTP sync. Returns offset in seconds.
    Falls back to 0.0 (no adjustment) if ntplib is missing or unreachable.
    """
    global _offset
    try:
        import ntplib
        client = ntplib.NTPClient()
        resp = client.request("pool.ntp.org", version=3)
        _offset = resp.offset
        direction = "behind" if _offset > 0 else "ahead"
        log.info(
            f"🕐 NTP sync: local clock is {abs(_offset):.3f}s {direction} of NTP"
        )
    except ImportError:
        log.warning("ntplib not installed — skipping NTP sync (pip install ntplib)")
    except Exception as e:
        log.warning(f"NTP sync failed ({e}) — using local clock, offset=0")
    return _offset


def now_adjusted() -> float:
    """Return current time corrected by NTP offset."""
    return time.time() + _offset


def perf_now() -> float:
    """High-resolution counter — unaffected by NTP offset. Use for elapsed time."""
    return time.perf_counter()
