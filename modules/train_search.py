"""
train_search.py — Fill search form + fire at the right moment.
  • NTP-adjusted clock (no drift at 10:00 AM)
  • Dead sleeps replaced with event-based polling
  • Structured logging + profiler
"""
import asyncio
import time
import nodriver as uc

from core.poller import wait_for_element, wait_for_elements, wait_for_js
from core.ntp import now_adjusted, perf_now
from core.logger import log
from core.profiler import timed
from config.selectors import (
    FROM_STATION_INPUT, TO_STATION_INPUT, AUTOCOMPLETE_ITEMS,
    DATE_INPUT, CALENDAR_MONTH, CALENDAR_YEAR, CALENDAR_NEXT, CALENDAR_DAYS,
    QUOTA_DROPDOWN, DROPDOWN_ITEMS, SEARCH_BTN,
)


# ─── Keyboard helpers ──────────────────────────────────────────────────────

async def press_key(tab, key, modifiers=0):
    KEY_CODES = {"Enter": 13, "Tab": 9, "Backspace": 8}
    code = KEY_CODES.get(key, 0)
    await tab.send(uc.cdp.input_.dispatch_key_event(
        type_="rawKeyDown", modifiers=modifiers,
        key=key, code=key, windows_virtual_key_code=code,
    ))
    await asyncio.sleep(0.04)
    await tab.send(uc.cdp.input_.dispatch_key_event(
        type_="keyUp", modifiers=modifiers,
        key=key, code=key, windows_virtual_key_code=code,
    ))


# ─── Date picker ──────────────────────────────────────────────────────────

MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

async def select_journey_date(tab, journey_date: str):
    day, month, year = map(int, journey_date.split("/"))

    date_input = await wait_for_element(tab, DATE_INPUT)
    await date_input.click()
    await wait_for_element(tab, CALENDAR_MONTH)

    current_month_text = await tab.evaluate(
        f"document.querySelector('{CALENDAR_MONTH}')?.textContent?.trim()"
    )
    current_year_text = await tab.evaluate(
        f"document.querySelector('{CALENDAR_YEAR}')?.textContent?.trim()"
    )

    current_month = MONTH_MAP.get(current_month_text, 0)
    current_year  = int(current_year_text)
    months_to_move = ((year - current_year) * 12) + (month - current_month)
    log.debug(f"Calendar: {current_month_text} {current_year} → navigate {months_to_move} months")

    for _ in range(months_to_move):
        next_btn = await wait_for_element(tab, CALENDAR_NEXT)
        await next_btn.click()
        # Wait for month header to update (replaces asyncio.sleep(0.2))
        await wait_for_js(tab, f"""
            (function() {{
                const t = document.querySelector('{CALENDAR_MONTH}')?.textContent?.trim();
                return t && t !== '{current_month_text}';
            }})()
        """, timeout=3)
        current_month_text = await tab.evaluate(
            f"document.querySelector('{CALENDAR_MONTH}')?.textContent?.trim()"
        )

    await wait_for_elements(tab, CALENDAR_DAYS, min_count=1)

    date_links = await tab.select_all(CALENDAR_DAYS)
    for idx, link in enumerate(date_links):
        text = await tab.evaluate(
            f"document.querySelectorAll('{CALENDAR_DAYS}')[{idx}].textContent?.trim()"
        )
        if text and text.isdigit() and int(text) == day:
            await link.click()
            log.info(f"✓ Date selected: {journey_date}")
            # Replace sleep(0.2) — wait for calendar to close
            await wait_for_js(tab, f"!document.querySelector('{CALENDAR_MONTH}')", timeout=3)
            return

    raise Exception(f"Day {day} not found in calendar")


# ─── Station autocomplete helper ──────────────────────────────────────────

async def fill_station(tab, selector: str, value: str, label: str):
    box = await wait_for_element(tab, selector)
    await box.click()
    await box.send_keys(value)
    await wait_for_element(tab, AUTOCOMPLETE_ITEMS)
    await tab.evaluate(f"""
        const item = document.querySelector('{AUTOCOMPLETE_ITEMS}');
        if (item) item.click();
    """)
    await press_key(tab, "Enter")
    await press_key(tab, "Tab")
    log.info(f"✓ {label}: {value}")


# ─── Fire clock ───────────────────────────────────────────────────────────

# async def _wait_for_fire_time(fire_time: str) -> None:
#     """Busy-wait using NTP-adjusted clock. Sends Telegram warning at T-30s."""
#     from datetime import datetime
#     from core.telegram import notify_fire_imminent

#     h, m, s = map(int, fire_time.split(":"))
#     target_epoch: float | None = None

#     while True:
#         now_ts = now_adjusted()
#         now_dt = datetime.fromtimestamp(now_ts)

#         if target_epoch is None:
#             # Compute target epoch for today
#             from datetime import date
#             today = date.today()
#             from datetime import datetime as dt
#             target_epoch = dt(today.year, today.month, today.day, h, m, s).timestamp()

#         remaining = target_epoch - now_ts

#         if remaining <= 0:
#             break

#         if 29.5 <= remaining <= 30.5:
#             log.info(f"⏰ T-30s warning — fire imminent")
#             asyncio.create_task(notify_fire_imminent(remaining))

#         await asyncio.sleep(0.015)   # ~15ms granularity — tighter than before

#     log.info("🚀 Fire time reached!")


# # ─── Main search function ─────────────────────────────────────────────────

# async def search_train(tab, route) -> float:
#     """
#     Fill search form, wait for fire_time, click Search.
#     Returns perf_counter() at the moment Search was clicked.
#     """
#     from_station  = route.from_station
#     to_station    = route.to_station
#     journey_date  = route.journey_date
#     fire_time     = route.fire_time
#     quota         = route.quota

#     async with timed("search_form_fill"):
#         log.info("Filling search form…")

#         await fill_station(tab, FROM_STATION_INPUT, from_station, "From")
#         await fill_station(tab, TO_STATION_INPUT,   to_station,   "To")
#         await select_journey_date(tab, journey_date)

#         # QUOTA dropdown
#         await wait_for_element(tab, QUOTA_DROPDOWN)
#         await tab.evaluate(f"document.querySelector('{QUOTA_DROPDOWN}').click();")
#         await wait_for_elements(tab, DROPDOWN_ITEMS, min_count=2)
#         await tab.evaluate(f"""
#             const items = document.querySelectorAll('{DROPDOWN_ITEMS}');
#             for (let item of items) {{
#                 if (item.textContent.trim() === '{quota}') {{
#                     item.click();
#                     break;
#                 }}
#             }}
#         """)
#         log.info(f"✓ Quota: {quota}")

#     # Wait for fire time (NTP-adjusted)
#     await _wait_for_fire_time(fire_time)

#     # SEARCH TRAINS
#     await wait_for_js(tab, f"""
#         [...document.querySelectorAll('{SEARCH_BTN}')]
#             .some(b => b.textContent.trim().includes('Search Trains'))
#     """)
#     await tab.evaluate(f"""
#         const btns = document.querySelectorAll('{SEARCH_BTN}');
#         for (let btn of btns) {{
#             if (btn.textContent.trim().includes('Search Trains')) {{
#                 btn.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true, cancelable: true }}));
#                 btn.dispatchEvent(new MouseEvent('mouseup',   {{ bubbles: true, cancelable: true }}));
#                 btn.dispatchEvent(new MouseEvent('click',     {{ bubbles: true, cancelable: true }}));
#                 break;
#             }}
#         }}
#     """)
#     log.info("✓ Search triggered")

#     return perf_now()
    # ─── Fire clock ───────────────────────────────────────────────────────────

async def _wait_for_fire_time(fire_time: str, offset_seconds: float = 0.0) -> None:
    """
    Busy-wait using NTP-adjusted clock.
    offset_seconds: fire this many seconds BEFORE the actual fire_time (default 0).
    Sends Telegram warning at T-30s.
    """
    from datetime import datetime, date
    from core.telegram import notify_fire_imminent

    h, m, s = map(int, fire_time.split(":"))
    target_epoch: float | None = None

    while True:
        now_ts = now_adjusted()

        if target_epoch is None:
            today = date.today()
            target_epoch = datetime(
                today.year, today.month, today.day, h, m, s
            ).timestamp() - offset_seconds  # ← shift target back by offset

        remaining = target_epoch - now_ts

        if remaining <= 0:
            break

        if 29.5 <= remaining <= 30.5:
            log.info(f"⏰ T-30s warning — fire imminent")
            asyncio.create_task(notify_fire_imminent(remaining))

        await asyncio.sleep(0.015)

    log.info(f"🚀 Fire time reached! (offset: -{offset_seconds}s)")


# ─── Main search function ─────────────────────────────────────────────────

async def search_train(tab, route) -> float:
    """
    Fill search form, wait for fire_time - 5s, click Search.
    Returns perf_counter() at the moment Search was clicked.
    """
    from_station  = route.from_station
    to_station    = route.to_station
    journey_date  = route.journey_date
    fire_time     = route.fire_time
    quota         = route.quota

    async with timed("search_form_fill"):
        log.info("Filling search form…")

        await fill_station(tab, FROM_STATION_INPUT, from_station, "From")
        await fill_station(tab, TO_STATION_INPUT,   to_station,   "To")
        await select_journey_date(tab, journey_date)

        # QUOTA dropdown
        await wait_for_element(tab, QUOTA_DROPDOWN)
        await tab.evaluate(f"document.querySelector('{QUOTA_DROPDOWN}').click();")
        await wait_for_elements(tab, DROPDOWN_ITEMS, min_count=2)
        await tab.evaluate(f"""
            const items = document.querySelectorAll('{DROPDOWN_ITEMS}');
            for (let item of items) {{
                if (item.textContent.trim() === '{quota}') {{
                    item.click();
                    break;
                }}
            }}
        """)
        log.info(f"✓ Quota: {quota}")

    # ⏰ Wait until fire_time MINUS 5 seconds, then click Search
    log.info(f"⏳ Waiting until {fire_time} - 5s to click Search…")
    await _wait_for_fire_time(fire_time, offset_seconds=5.0)

    # SEARCH TRAINS
    await wait_for_js(tab, f"""
        [...document.querySelectorAll('{SEARCH_BTN}')]
            .some(b => b.textContent.trim().includes('Search Trains'))
    """)
    await tab.evaluate(f"""
        const btns = document.querySelectorAll('{SEARCH_BTN}');
        for (let btn of btns) {{
            if (btn.textContent.trim().includes('Search Trains')) {{
                btn.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true, cancelable: true }}));
                btn.dispatchEvent(new MouseEvent('mouseup',   {{ bubbles: true, cancelable: true }}));
                btn.dispatchEvent(new MouseEvent('click',     {{ bubbles: true, cancelable: true }}));
                break;
            }}
        }}
    """)
    log.info("✓ Search triggered (5s before fire time)")

    return perf_now()
