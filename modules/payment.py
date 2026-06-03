"""
payment.py — Automate IRCTC payment page.
Supports:
    - UPI (auto-select saved VPA)
    - IRCTC E-Wallet
    - Manual fallback
Polls for PNR confirmation and extracts it.
"""

import asyncio

from core.poller import wait_for_element, wait_for_js, wait_for_url_contains
from core.logger import log
from core.profiler import timed
from config.selectors import (
    PAYMENT_UPI_OPTION,
    SAVED_UPI_DROPDOWN,
    PAY_NOW_BTN,
    PNR_CONFIRM_TEXT,
    IRCTC_TIMEOUT_MODAL,
)


async def _handle_irctc_timeout(tab) -> bool:
    """Check for IRCTC session timeout modal and dismiss if present."""
    try:
        modal = await tab.evaluate(
            f"!!document.querySelector('{IRCTC_TIMEOUT_MODAL}')"
        )

        if modal:
            log.warning("⚠ IRCTC timeout modal detected — attempting dismiss")

            await tab.evaluate(f"""
                const btn = document.querySelector('{IRCTC_TIMEOUT_MODAL} button');
                if (btn) btn.click();
            """)

            return True

    except Exception:
        pass

    return False


async def _extract_pnr(tab) -> str:
    """Try to extract PNR from confirmation page."""
    try:
        pnr = await tab.evaluate(f"""
            (() => {{
                const el = document.querySelector('{PNR_CONFIRM_TEXT}');
                return el ? el.textContent.trim() : null;
            }})()
        """)

        return pnr or "UNKNOWN"

    except Exception:
        return "UNKNOWN"


async def automate_payment(tab, payment_config) -> str:
    """
    Navigate the payment page and confirm booking.

    payment_config fields:
        method:
            UPI
            EWALLET
            CARD
            NETBANKING
            MANUAL
    
        saved_upi_id:
            user@upi
    """

    async with timed("payment"):

        method = payment_config.method.upper()
        saved_upi_id = getattr(payment_config, "saved_upi_id", None)

        log.info(f"💳 Payment page — method: {method}")

        await wait_for_js(
            tab,
            """
            window.location.href.includes('payment') ||
            window.location.href.includes('booking') ||
            document.title.toLowerCase().includes('payment')
            """,
            timeout=30,
        )

        await _handle_irctc_timeout(tab)

        if method == "MANUAL":

            log.info("⏸ Payment set to MANUAL")
            input(">>> Complete payment manually, then press Enter... ")

        elif method == "UPI":

            await _pay_upi(tab, saved_upi_id)

        elif method == "EWALLET":

            await _pay_ewallet(tab)

        else:

            log.warning(
                f"Payment method '{method}' not automated — manual action required"
            )

            input(">>> Complete payment manually, then press Enter... ")

        log.info("⏳ Waiting for booking confirmation...")

        pnr = await _wait_for_confirmation(tab)

        log.info(f"🎉 Booking confirmed! PNR: {pnr}")

        return pnr


async def _pay_upi(tab, saved_upi_id: str) -> None:
    """Select UPI and click Pay Now."""

    try:
        await wait_for_element(tab, PAYMENT_UPI_OPTION, timeout=10)

        await tab.evaluate(f"""
            const el = document.querySelector('{PAYMENT_UPI_OPTION}');
            if (el) el.click();
        """)

        log.info("✓ UPI option selected")

    except TimeoutError:

        log.warning("UPI option not found")

    if saved_upi_id:

        try:
            await wait_for_element(tab, SAVED_UPI_DROPDOWN, timeout=5)

            await tab.evaluate(f"""
                (() => {{
                    const sel = document.querySelector('{SAVED_UPI_DROPDOWN}');
                    if (!sel) return;

                    const opts = [...sel.options];

                    const opt = opts.find(
                        o =>
                            o.text.includes('{saved_upi_id}') ||
                            o.value.includes('{saved_upi_id}')
                    );

                    if (opt) {{
                        sel.value = opt.value;
                        sel.dispatchEvent(
                            new Event('change', {{ bubbles: true }})
                        );
                    }}
                }})()
            """)

            log.info(f"✓ Saved UPI selected: {saved_upi_id}")

        except TimeoutError:

            log.warning("Saved UPI dropdown not found")

    await wait_for_element(tab, PAY_NOW_BTN, timeout=10)

    await tab.evaluate(f"""
        const btn = document.querySelector('{PAY_NOW_BTN}');

        if (btn) {{
            btn.dispatchEvent(
                new MouseEvent('mousedown', {{ bubbles: true }})
            );

            btn.dispatchEvent(
                new MouseEvent('mouseup', {{ bubbles: true }})
            );

            btn.dispatchEvent(
                new MouseEvent('click', {{ bubbles: true }})
            );
        }}
    """)

    log.info("✓ Pay Now clicked")




# async def _pay_ewallet(tab) -> None:
#     """
#     Select IRCTC E-Wallet and click Pay & Book.
#     """

#     log.info("💰 Selecting IRCTC E-Wallet")

#     # Give Angular time to render payment methods
#     await asyncio.sleep(3)

#     # Debug: print all visible payment options
#     try:
#         payment_options = await tab.evaluate("""
#         (() => {
#             return [...document.querySelectorAll('.bank-type')]
#                 .map(x => x.innerText.trim())
#                 .filter(Boolean);
#         })()
#         """)
#         log.info(f"Available payment methods: {payment_options}")
#     except Exception:
#         pass

#     selected = await tab.evaluate("""
#     (() => {

#         const options =
#             [...document.querySelectorAll('.bank-type')];

#         const ewallet = options.find(el => {

#             const img = el.querySelector('img');

#             return (
#                 (img &&
#                  img.src &&
#                  img.src.includes('IrctcEWallet'))
#                 ||
#                 (el.textContent &&
#                  el.textContent.includes('E-Wallet'))
#             );
#         });

#         if (!ewallet)
#             return false;

#         ewallet.scrollIntoView({
#             block: 'center',
#             behavior: 'instant'
#         });

#         ewallet.click();

#         ewallet.dispatchEvent(
#             new MouseEvent('click', {
#                 bubbles: true,
#                 cancelable: true,
#                 view: window
#             })
#         );

#         return true;
#     })()
#     """)

#     if not selected:
#         raise Exception(
#             "E-Wallet option not found on payment page"
#         )

#     log.info("✓ E-Wallet selected")

#     await asyncio.sleep(2)

#     clicked = await tab.evaluate("""
#     (() => {

#         const buttons =
#             [...document.querySelectorAll('button')];

#         let payBtn = buttons.find(btn =>
#             btn.textContent &&
#             btn.textContent.trim() === 'Pay & Book'
#         );

#         if (!payBtn) {

#             payBtn = buttons.find(btn =>
#                 btn.textContent &&
#                 btn.textContent.includes('Pay')
#             );
#         }

#         if (!payBtn)
#             return false;

#         payBtn.scrollIntoView({
#             block: 'center',
#             behavior: 'instant'
#         });

#         payBtn.click();

#         payBtn.dispatchEvent(
#             new MouseEvent('click', {
#                 bubbles: true,
#                 cancelable: true,
#                 view: window
#             })
#         );

#         return true;
#     })()
#     """)

#     if not clicked:
#         raise Exception(
#             "Pay & Book button not found"
#         )

#     log.info("✓ Pay & Book clicked")

async def _pay_ewallet(tab) -> None:
    """
    Select IRCTC E-Wallet and click Pay & Book.
    Ensures IRCTC iPay is NOT used.
    """

    log.info("💰 Selecting IRCTC E-Wallet")

    # Let Angular finish rendering
    await asyncio.sleep(2)

    selected = await tab.evaluate("""
    (() => {

        const ewallet =
            [...document.querySelectorAll('.bank-type')]
            .find(el =>
                el.textContent &&
                el.textContent.includes('E-Wallet')
            );

        if (!ewallet)
            return false;

        ewallet.scrollIntoView({
            block: 'center'
        });

        ewallet.click();

        return true;

    })()
    """)

    if not selected:
        raise Exception(
            "E-Wallet option not found"
        )

    log.info("✓ E-Wallet clicked")

    #
    # Wait for Angular to switch active payment mode
    #
    await asyncio.sleep(1.5)

    active = await tab.evaluate("""
    (() => {

        const active =
            document.querySelector('.bank-type-active');

        if (!active)
            return false;

        return active.textContent.includes('E-Wallet');

    })()
    """)

    if not active:
        raise Exception(
            "Failed to switch from IRCTC iPay to E-Wallet"
        )

    log.info("✓ E-Wallet is active")

    #
    # Extra verification:
    # ensure IRCTC iPay is NOT active
    #
    ipay_active = await tab.evaluate("""
    (() => {

        const active =
            document.querySelector('.bank-type-active');

        if (!active)
            return false;

        return active.textContent.includes('IRCTC iPay');

    })()
    """)

    if ipay_active:
        raise Exception(
            "IRCTC iPay is still active"
        )

    #
    # Click Pay & Book
    #
    clicked = await tab.evaluate("""
    (() => {

        const buttons =
            [...document.querySelectorAll('button')];

        const payBtn = buttons.find(btn =>
            btn.textContent &&
            btn.textContent.trim() === 'Pay & Book'
        );

        if (!payBtn)
            return false;

        payBtn.scrollIntoView({
            block: 'center'
        });

        payBtn.click();

        return true;

    })()
    """)

    if not clicked:
        raise Exception(
            "Pay & Book button not found"
        )

    log.info("✓ Pay & Book clicked")
async def _wait_for_confirmation(tab) -> str:
    """
    Poll for PNR on confirmation page.
    """

    elapsed = 0.0

    while elapsed < 120:

        await _handle_irctc_timeout(tab)

        pnr_present = await tab.evaluate(
            f"!!document.querySelector('{PNR_CONFIRM_TEXT}')"
        )

        if pnr_present:
            return await _extract_pnr(tab)

        url = await tab.evaluate(
            "window.location.href"
        )

        if any(
            x in url
            for x in (
                "booking-history",
                "printTicket",
                "pnr",
            )
        ):
            return await _extract_pnr(tab)

        await asyncio.sleep(0.5)

        elapsed += 0.5

    log.error("⚠ Confirmation page not reached within 120 seconds")

    return "TIMEOUT"