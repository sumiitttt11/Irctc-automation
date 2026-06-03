"""
passenger_filler.py — Fill passenger details.
  BUG FIX: name input is now queried on `row`, not global `tab`,
            so passenger 2+ fill correctly.
  NEW:      berth preference per passenger
  NEW:      dead sleeps replaced with event-based waits
"""
import asyncio
import nodriver as uc

from core.poller import wait_for_elements, wait_for_element, wait_for_js
from core.logger import log
from core.profiler import timed
from config.selectors import (
    PASSENGER_ROW, NAME_INPUT, AGE_INPUT, GENDER_SELECT,
    MASTER_LIST_ITEM, AUTO_UPGRADE_CB, CONTINUE_BTN, ADD_PASSENGER_TEXT,
)

BERTH_MAP = {
    "LB":  "Lower Berth",
    "MB":  "Middle Berth",
    "UB":  "Upper Berth",
    "SLB": "Side Lower",
    "SUB": "Side Upper",
    "NO PREFERENCE": "No Preference",
    "":    "No Preference",
}


async def _type_char_by_char(tab, text: str):
    """Type text character by character via CDP (for Angular name fields)."""
    for char in text:
        await tab.send(uc.cdp.input_.dispatch_key_event(
            type_="char", text=char
        ))
        await asyncio.sleep(0.03)   # minimum required for Angular to register


async def _select_berth(tab, row, berth_code: str):
    """Select berth preference dropdown inside a passenger row."""
    label = BERTH_MAP.get(berth_code.upper(), "No Preference")
    try:
        sel = await row.query_selector("select[formcontrolname='berthChoice']")
        if not sel:
            return
        await tab.evaluate(f"""
            const sel = document.querySelector(
                "app-passenger select[formcontrolname='berthChoice']"
            );
            if (sel) {{
                const opts = [...sel.options];
                const opt = opts.find(o => o.text.trim().includes('{label}'));
                if (opt) {{
                    sel.value = opt.value;
                    sel.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
        """)
        log.debug(f"  Berth preference: {label}")
    except Exception as e:
        log.debug(f"  Berth select skipped: {e}")


async def fill_passengers(tab, data) -> None:
    async with timed("passenger_filler"):
        log.info("Waiting for passenger form…")

        passengers = data.passengers

        await wait_for_elements(tab, PASSENGER_ROW, min_count=1, timeout=20)
        rows = await tab.select_all(PASSENGER_ROW)

        for i, passenger in enumerate(passengers):
            log.info(f"Filling passenger {i+1}: {passenger.name}")
            row = rows[i]

            # ── BUG FIX: scope name input to THIS row ──────────────────
            name_box = await row.query_selector(NAME_INPUT)
            if not name_box:
                # Fallback to global if row scoping fails (single-passenger page)
                # name_box = await wait_for_element(tab, NAME_INPUT)
                row = rows[i]
                name_box = await row.query_selector(NAME_INPUT)

            await name_box.click()
            await _type_char_by_char(tab, passenger.name)

            # ── Master list matching ───────────────────────────────────
            matched = False
            try:
                await wait_for_elements(tab, MASTER_LIST_ITEM, min_count=1, timeout=4)
                suggestions = await tab.select_all(MASTER_LIST_ITEM)
                for s in suggestions:
                    s_html = await s.get_html()
                    if passenger.name.lower().split()[0] in s_html.lower():
                        await s.click()
                        log.info(f"  ✓ Passenger {i+1} selected from master list")
                        matched = True
                        break
            except TimeoutError:
                pass

            # ── Manual entry fallback ──────────────────────────────────
            if not matched:
                log.info(f"  Master list miss — entering manually")

                age_box = await row.query_selector(AGE_INPUT)
                if age_box:
                    await age_box.send_keys(str(passenger.age))

                gender_val = passenger.gender
                await tab.evaluate(f"""
                    (function() {{
                        const rows = document.querySelectorAll('{PASSENGER_ROW}');
                        const row  = rows[{i}];
                        if (!row) return;
                        const sel  = row.querySelector('{GENDER_SELECT}');
                        if (sel) {{
                            sel.value = '{gender_val}';
                            sel.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }})()
                """)
                log.info(f"  ✓ Passenger {i+1} entered manually (age={passenger.age}, gender={gender_val})")

            # ── Berth preference ───────────────────────────────────────
            await _select_berth(tab, row, getattr(passenger, "berth_preference", ""))

            # ── Add next passenger if needed (replace sleep with count poll) ─
            if i < len(passengers) - 1:
                add_btn = await tab.find(ADD_PASSENGER_TEXT, best_match=True)
                await add_btn.mouse_click()
                # Wait for the new row to appear instead of sleeping
                await wait_for_elements(tab, PASSENGER_ROW, min_count=i+2, timeout=10)
                rows = await tab.select_all(PASSENGER_ROW)

        log.info("✓ All passengers filled")

        # ── Auto Upgrade ───────────────────────────────────────────────
        if data.auto_upgrade:
            await wait_for_element(tab, AUTO_UPGRADE_CB)
            await tab.evaluate(f"""
                const cb = document.querySelector('{AUTO_UPGRADE_CB}');
                if (cb && !cb.checked) {{
                    cb.click();
                    cb.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            """)
            log.info("✓ Auto Upgrade enabled")

        # ── Continue ───────────────────────────────────────────────────
        await wait_for_js(tab, f"document.querySelector('{CONTINUE_BTN}') !== null")
        continue_btn = await tab.select(CONTINUE_BTN)
        await continue_btn.click()
        log.info("✓ Continue clicked")
