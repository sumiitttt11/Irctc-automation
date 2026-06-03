"""
health_check.py — Pre-fire health checks.
Validates everything before the browser even launches so you don't
discover a typo at 10:00:00 AM.
"""
import os
import sys
import shutil
from pathlib import Path

from core.logger import log


def run_checks(route, passengers) -> None:
    """Run all checks. Raises SystemExit on any failure."""
    errors = []

    # ── Credentials ────────────────────────────────────────────────────
    username = os.getenv("IRCTC_USERNAME", "")
    password = os.getenv("IRCTC_PASSWORD", "")
    if not username:
        errors.append("IRCTC_USERNAME not set in .env")
    if not password:
        errors.append("IRCTC_PASSWORD not set in .env")

    # ── Storage dirs ───────────────────────────────────────────────────
    for d in ("storage/screenshots", "logs"):
        Path(d).mkdir(parents=True, exist_ok=True)

    # ── nodriver importable ────────────────────────────────────────────
    try:
        import nodriver  # noqa: F401
    except ImportError:
        errors.append("nodriver not installed — run: pip install nodriver")

    # ── Chrome / Chromium available ────────────────────────────────────
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        log.warning("⚠  Chrome/Chromium not found in PATH — nodriver may still locate it")

    # ── Route sanity ───────────────────────────────────────────────────
    if route.from_station == route.to_station:
        errors.append(f"from_station == to_station: '{route.from_station}'")

    # ── Passenger count ────────────────────────────────────────────────
    if len(passengers.passengers) == 0:
        errors.append("No passengers defined")
    if len(passengers.passengers) > 6:
        errors.append("IRCTC max 6 passengers per booking")

    # ── Telegram (optional) ────────────────────────────────────────────
    tok = os.getenv("TELEGRAM_BOT_TOKEN", "")
    cid = os.getenv("TELEGRAM_CHAT_ID", "")
    if bool(tok) != bool(cid):
        log.warning("⚠  Telegram: set both TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
    if tok and cid:
        log.info("✓ Telegram notifications: enabled")
    else:
        log.info("ℹ  Telegram notifications: disabled (optional)")

    # ── Captcha key (optional) ─────────────────────────────────────────
    if os.getenv("CAPTCHA_API_KEY"):
        log.info("✓ 2captcha auto-solver: enabled")
    else:
        log.info("ℹ  2captcha: disabled — will pause for manual CAPTCHA solve")

    # ── Report ─────────────────────────────────────────────────────────
    if errors:
        print("\n❌ Pre-flight checks FAILED:\n")
        for e in errors:
            print(f"   • {e}")
        print()
        sys.exit(1)

    log.info("✅ Pre-flight checks passed")
    log.info(f"   Route     : {route.from_station} → {route.to_station} on {route.journey_date}")
    log.info(f"   Trains    : {[t.number for t in route.trains]}")
    log.info(f"   Fire time : {route.fire_time}")
    log.info(f"   Passengers: {len(passengers.passengers)}")
