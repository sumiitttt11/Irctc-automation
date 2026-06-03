# """
# train_selector.py — select train card + class + availability, click Book Now.
#   • Multi-train fallback (tries next train if first not found / full)
#   • Multi-class fallback per train (e.g. SL → 3A)
#   • Structured logging + profiler
# """
# import asyncio

# from core.poller import wait_for_elements, wait_for_js  # wait_for_js used in Book Now poll below
# from core.logger import log
# from core.profiler import timed
# from config.selectors import TRAIN_CARDS, CLASS_BOX, BOOK_NOW_BTN



# CLASS_MAP = {
#     "SL": "Sleeper (SL)",
#     "3A": "AC 3 Tier (3A)",
#     "2A": "AC 2 Tier (2A)",
#     "1A": "AC First Class (1A)",
#     "CC": "AC Chair car (CC)",
#     "EC": "Exec. Chair Car (EC)",
# }


# async def _try_book(tab, card, train_number: str, travel_class: str) -> bool:
#     """
#     Attempt to select class + availability and click Book Now on a given card.
#     Returns True on success, False if class/availability not found.
#     """
#     class_text = CLASS_MAP.get(travel_class)
#     if not class_text:
#         log.warning(f"Unknown class code: {travel_class}")
#         return False

#     MAX_CLASS_RETRIES = 3

#     for attempt in range(1, MAX_CLASS_RETRIES + 1):
#         # Select class
#         class_boxes = await card.query_selector_all(CLASS_BOX)
#         class_found = False
#         for box in class_boxes:
#             box_html = await box.get_html()
#             if class_text in box_html:
#                 await box.click()
#                 class_found = True
#                 break

#         if not class_found:
#             log.debug(f"  Class {travel_class} not found on train {train_number}")
#             return False

#         log.info(f"  ✓ Class {travel_class} selected (attempt {attempt})")

#         # Poll until an AVAILABLE box appears inside this card.
#         # 8s window — Angular needs time to re-render availability after class click.
#         avl_found = False
#         elapsed = 0.0
#         while elapsed < 8.0:
#             avl_boxes = await card.query_selector_all(CLASS_BOX)
#             for box in avl_boxes:
#                 box_html = await box.get_html()
#                 if "AVAILABLE" in box_html:
#                     await box.click()
#                     avl_found = True
#                     break
#             if avl_found:
#                 break
#             await asyncio.sleep(0.15)
#             elapsed += 0.15

#         if avl_found:
#             break  # Exit retry loop — availability found and clicked

#         # No availability appeared — retry clicking the class button
#         if attempt < MAX_CLASS_RETRIES:
#             log.warning(
#                 f"  No AVAILABLE seats after class click (attempt {attempt}/{MAX_CLASS_RETRIES}), retrying class click..."
#             )
#         else:
#             log.warning(
#                 f"  No AVAILABLE seats for {travel_class} on train {train_number} after {MAX_CLASS_RETRIES} attempts"
#             )
#             return False

#     log.info("  ✓ Availability selected")

#     # Wait for Book Now
#     await wait_for_js(tab, """
#         [...(document.querySelectorAll('app-train-avl-enq button') || [])]
#             .some(b => b.textContent.includes('Book Now'))
#     """, timeout=10)

#     # Click Book Now immediately once found
#     buttons = await card.query_selector_all(BOOK_NOW_BTN)
#     for btn in buttons:
#         btn_html = await btn.get_html()
#         if "Book Now" in btn_html:
#             await btn.click()
#             log.info(f"  ✓ Book Now clicked — Train {train_number} | {travel_class}")
#             return True

#     return False

# async def select_train(tab, route) -> None:
#     """
#     Try each train in route.trains[]; for each train try each class in order.
#     Raises if no train/class combination succeeds.
#     """
#     async with timed("train_selector"):
#         log.info("Waiting for train list…")
#         await wait_for_elements(tab, TRAIN_CARDS, min_count=1, timeout=30)

#         cards = await tab.select_all(TRAIN_CARDS)
#         log.info(f"Found {len(cards)} train cards")

#         for train_opt in route.trains:
#             train_number = train_opt.number
#             log.info(f"🔍 Looking for train {train_number}…")

#             # Find the card for this train
#             target_card = None
#             for card in cards:
#                 card_html = await card.get_html()
#                 if f"({train_number})" in card_html:
#                     target_card = card
#                     break

#             if target_card is None:
#                 log.warning(f"  Train {train_number} not in results — trying next fallback")
#                 continue

#             log.info(f"  ✓ Train {train_number} found")
#             await target_card.scroll_into_view()
#             # Replace sleep(0.5) with a short visibility settle (intentional)
#             await asyncio.sleep(0.15)

#             # Try each class in the preference order
#             for cls in train_opt.classes:
#                 booked = await _try_book(tab, target_card, train_number, cls)
#                 if booked:
#                     return

#         raise Exception(
#             f"Could not book any train. Tried: "
#             + ", ".join(f"{t.number}({'/'.join(t.classes)})" for t in route.trains)
#         )

import asyncio
from datetime import datetime

from core.poller import wait_for_elements, wait_for_js
from core.logger import log
from core.profiler import timed
from config.selectors import TRAIN_CARDS, CLASS_BOX, BOOK_NOW_BTN


CLASS_MAP = {
    "SL": "Sleeper (SL)",
    "3A": "AC 3 Tier (3A)",
    "2A": "AC 2 Tier (2A)",
    "1A": "AC First Class (1A)",
    "CC": "AC Chair car (CC)",
    "EC": "Exec. Chair Car (EC)",
}


async def _wait_until_fire_time(fire_time_str: str):
    """
    Waits until the specified fire_time (HH:MM:SS) today.
    If fire_time has already passed, proceeds immediately.
    """
    now = datetime.now()
    h, m, s = map(int, fire_time_str.split(":"))
    fire_dt = now.replace(hour=h, minute=m, second=s, microsecond=0)

    wait_seconds = (fire_dt - now).total_seconds()
    if wait_seconds > 0:
        log.info(f"  ⏳ Waiting {wait_seconds:.2f}s until fire time {fire_time_str}...")
        await asyncio.sleep(wait_seconds)
    else:
        log.info(f"  ⚡ Fire time {fire_time_str} already reached, proceeding immediately.")


async def _try_book(tab, card, train_number: str, travel_class: str) -> bool:
    """
    Attempt to select class + availability and click Book Now on a given card.
    Returns True on success, False if class/availability not found.
    """
    class_text = CLASS_MAP.get(travel_class)
    if not class_text:
        log.warning(f"Unknown class code: {travel_class}")
        return False

    MAX_CLASS_RETRIES = 3

    for attempt in range(1, MAX_CLASS_RETRIES + 1):
        # Select class
        class_boxes = await card.query_selector_all(CLASS_BOX)
        class_found = False
        for box in class_boxes:
            box_html = await box.get_html()
            if class_text in box_html:
                await box.click()
                class_found = True
                break

        if not class_found:
            log.debug(f"  Class {travel_class} not found on train {train_number}")
            return False

        log.info(f"  ✓ Class {travel_class} selected (attempt {attempt})")

        # Poll until an AVAILABLE box appears inside this card.
        # 8s window — Angular needs time to re-render availability after class click.
        avl_found = False
        elapsed = 0.0
        while elapsed < 8.0:
            avl_boxes = await card.query_selector_all(CLASS_BOX)
            for box in avl_boxes:
                box_html = await box.get_html()
                if "AVAILABLE" in box_html:
                    await box.click()
                    avl_found = True
                    break
            if avl_found:
                break
            await asyncio.sleep(0.15)
            elapsed += 0.15

        if avl_found:
            break  # Exit retry loop — availability found and clicked

        # No availability appeared — retry clicking the class button
        if attempt < MAX_CLASS_RETRIES:
            log.warning(
                f"  No AVAILABLE seats after class click (attempt {attempt}/{MAX_CLASS_RETRIES}), retrying class click..."
            )
        else:
            log.warning(
                f"  No AVAILABLE seats for {travel_class} on train {train_number} after {MAX_CLASS_RETRIES} attempts"
            )
            return False

    log.info("  ✓ Availability selected")

    # Wait for Book Now
    await wait_for_js(tab, """
        [...(document.querySelectorAll('app-train-avl-enq button') || [])]
            .some(b => b.textContent.includes('Book Now'))
    """, timeout=10)

    # Click Book Now immediately once found
    buttons = await card.query_selector_all(BOOK_NOW_BTN)
    for btn in buttons:
        btn_html = await btn.get_html()
        if "Book Now" in btn_html:
            await btn.click()
            log.info(f"  ✓ Book Now clicked — Train {train_number} | {travel_class}")
            return True

    return False


async def select_train(tab, route) -> None:
    """
    Try each train in route.trains[]; for each train try each class in order.
    Raises if no train/class combination succeeds.
    """
    async with timed("train_selector"):
        log.info("Waiting for train list…")
        await wait_for_elements(tab, TRAIN_CARDS, min_count=1, timeout=30)

        cards = await tab.select_all(TRAIN_CARDS)
        log.info(f"Found {len(cards)} train cards")

        # Pre-locate all target cards before fire_time so we're ready to act instantly
        train_card_map = {}
        for train_opt in route.trains:
            train_number = train_opt.number
            log.info(f"🔍 Looking for train {train_number}…")

            for card in cards:
                card_html = await card.get_html()
                if f"({train_number})" in card_html:
                    train_card_map[train_number] = (card, train_opt)
                    log.info(f"  ✓ Train {train_number} found — will book at fire time")
                    break
            else:
                log.warning(f"  Train {train_number} not in results — skipping")

        if not train_card_map:
            raise Exception(
                f"Could not find any target trains. Tried: "
                + ", ".join(t.number for t in route.trains)
            )

        # ⏰ Wait until fire_time — one shared wait for all trains
        await _wait_until_fire_time(route.fire_time)

        # Now attempt booking in preference order
        for train_opt in route.trains:
            train_number = train_opt.number

            if train_number not in train_card_map:
                continue

            target_card, _ = train_card_map[train_number]
            await target_card.scroll_into_view()
            await asyncio.sleep(0.15)

            for cls in train_opt.classes:
                booked = await _try_book(tab, target_card, train_number, cls)
                if booked:
                    return

        raise Exception(
            f"Could not book any train. Tried: "
            + ", ".join(f"{t.number}({'/'.join(t.classes)})" for t in route.trains)
        )