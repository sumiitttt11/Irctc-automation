"""
main.py — Tatkal booking orchestrator.

Full flow:
  Pre-flight → Browser → Login (session reuse) → Form fill →
  ⏱ Fire clock (NTP) → Search → Select train → Fill passengers →
  💳 Payment → PNR → 📲 Telegram notification
"""
import asyncio
import traceback
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from core.logger import log
from core.ntp import sync_clock
from core.browser import create_browser
from core.config_loader import load_and_validate_route, load_and_validate_passengers
from core.profiler import print_summary
from core.retry import _take_screenshot

from modules.health_check import run_checks
from modules.login import fill_login
from modules.train_search import search_train
from modules.train_selector import select_train
from modules.passenger_filler import fill_passengers
from modules.payment import automate_payment
# from modules.review_page import wait_for_user_captcha
from modules.review_page import fill_captcha_page

async def main():
    # ── Load + validate configs ────────────────────────────────────────
    route      = load_and_validate_route("config/routes.json")
    passengers = load_and_validate_passengers("config/passengers.json")

    # ── Pre-flight health checks ───────────────────────────────────────
    run_checks(route, passengers)

    # ── NTP clock sync ─────────────────────────────────────────────────
    sync_clock()

    browser, tab = await create_browser()

    try:
        # ── Login (tries saved session first) ──────────────────────────
        await fill_login(tab)

        # ── Fill search form + wait for fire time + click Search ───────
        search_start = await search_train(tab, route)

        # ── Select train + class (with fallback) ───────────────────────
        await select_train(tab, route)

        # ── Fill passenger details ─────────────────────────────────────
        await fill_passengers(tab, passengers)

        # await wait_for_user_captcha(tab)
        await fill_captcha_page(tab)

        # ── Payment ────────────────────────────────────────────────────
        pnr = await automate_payment(tab, route.payment)

        # ── Success notification ───────────────────────────────────────
        from core.telegram import notify_success
        pax_names = [p.name for p in passengers.passengers]
        await notify_success(
            pnr=pnr,
            train=route.trains[0].number,
            travel_class=route.trains[0].classes[0],
            passengers=pax_names,
        )

        log.info(f"\n{'='*50}")
        log.info(f"  🎉 BOOKING COMPLETE — PNR: {pnr}")
        log.info(f"{'='*50}\n")

    except Exception as exc:
        log.error(f"❌ Run failed: {exc}")
        log.debug(traceback.format_exc())

        # Screenshot on crash
        try:
            await _take_screenshot(tab, "final_crash")
        except Exception:
            pass

        # Failure notification
        try:
            latest_screenshot = sorted(
                Path("storage/screenshots").glob("*.png"),
                key=lambda p: p.stat().st_mtime
            )
            screenshot_path = str(latest_screenshot[-1]) if latest_screenshot else None
            from core.telegram import notify_failure
            await notify_failure(str(exc), screenshot_path)
        except Exception:
            pass

        raise

    finally:
        print_summary()
        input("\nPress Enter to close browser… ")


if __name__ == "__main__":
    asyncio.run(main())
