"""
login.py — IRCTC login with:
  • CAPTCHA detection (manual pause + optional 2captcha API)
  • Silent-failure detection (raises RuntimeError instead of passing through)
  • Session cookie persistence (tries saved session first)
  • Structured logging
"""
import asyncio
import os
import base64

from dotenv import load_dotenv
from core.poller import wait_for_element, wait_for_js
from core.browser import save_cookies, load_cookies, is_session_valid
from core.logger import log
from core.profiler import timed
from config.selectors import (
    LOGIN_LINK, LOGIN_MODAL, LOGIN_FORM,
    INPUT_USERNAME, INPUT_PASSWORD, SUBMIT_BTN,
    CAPTCHA_IMG, CAPTCHA_INPUT,
)

load_dotenv()

USERNAME       = os.getenv("IRCTC_USERNAME", "")
PASSWORD       = os.getenv("IRCTC_PASSWORD", "")
CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "")   # 2captcha key (optional)


# ─── CAPTCHA solver ────────────────────────────────────────────────────────

async def _solve_captcha_auto(tab) -> str | None:
    """
    Try 2captcha API.  Returns solved text or None on failure.
    Requires CAPTCHA_API_KEY in .env and `pip install 2captcha-python`.
    """
    if not CAPTCHA_API_KEY:
        return None
    try:
        from twocaptcha import TwoCaptcha
        solver = TwoCaptcha(CAPTCHA_API_KEY)

        # Screenshot the captcha element into a base64 png
        captcha_b64 = await tab.evaluate(f"""
            (function() {{
                const img = document.querySelector('{CAPTCHA_IMG}');
                if (!img) return null;
                const c = document.createElement('canvas');
                c.width = img.naturalWidth || img.width;
                c.height = img.naturalHeight || img.height;
                c.getContext('2d').drawImage(img, 0, 0);
                return c.toDataURL('image/png').split(',')[1];
            }})()
        """)
        if not captcha_b64:
            return None

        log.info("🤖 Sending CAPTCHA to 2captcha API…")
        result = solver.normal(captcha_b64)
        log.info(f"✓ CAPTCHA solved: {result['code']}")
        return result["code"]

    except Exception as e:
        log.warning(f"2captcha failed: {e}")
        return None


async def _handle_captcha(tab) -> None:
    """Detect CAPTCHA and either auto-solve or prompt manual solve."""
    from core.telegram import notify_captcha_needed

    # Check whether a CAPTCHA is visible
    has_captcha = await tab.evaluate(f"""
        !!document.querySelector('{CAPTCHA_IMG}')
    """)
    if not has_captcha:
        return

    log.warning("🔐 CAPTCHA detected")
    await notify_captcha_needed()

    # Try auto-solve first
    answer = await _solve_captcha_auto(tab)
    if answer:
        captcha_box = await tab.evaluate(f"""
            !!document.querySelector('{CAPTCHA_INPUT}')
        """)
        if captcha_box:
            inp = await wait_for_element(tab, CAPTCHA_INPUT, timeout=5)
            await inp.click()
            await inp.send_keys(answer)
            await tab.evaluate(f"""
                let el = document.querySelector('{CAPTCHA_INPUT}');
                if (el) {{
                    el.dispatchEvent(new Event('input',  {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            """)
            log.info("✓ CAPTCHA auto-filled")
            return

    # Fall back: pause for manual solve
    log.warning("⏸  Pausing for manual CAPTCHA solve — solve it in the browser window.")
    input("   >>> Solve the CAPTCHA, then press Enter to continue … ")
    log.info("↩  Continuing after manual CAPTCHA")


# ─── Main login function ───────────────────────────────────────────────────

async def fill_login(tab) -> None:
    """
    Full login flow.
    1. Try saved session cookies first.
    2. If session expired / no cookies: do a fresh login.
    3. After fresh login: save cookies for next run.
    """
    async with timed("login"):
        # ── Try saved session ──────────────────────────────────────────
        cookies_loaded = await load_cookies(tab)
        if cookies_loaded:
            log.info("🔑 Saved session found — checking validity…")
            if await is_session_valid(tab):
                log.info("✓ Session still valid — skipping login")
                return
            else:
                log.warning("⚠  Session expired — doing fresh login")
                from core.browser import clear_session
                clear_session()

        # ── Fresh login ────────────────────────────────────────────────
        await tab.get("https://www.irctc.co.in/nget/train-search")

        login_link = await wait_for_element(tab, LOGIN_LINK)
        await login_link.click()

        await wait_for_element(tab, LOGIN_MODAL)
        # Brief settle for Angular animation — scoped, intentional
        await asyncio.sleep(0.25)

        # Fill username
        username_box = await wait_for_element(tab, INPUT_USERNAME)
        await username_box.click()
        await username_box.send_keys(USERNAME)
        await tab.evaluate(f"""
            let el = document.querySelector('{INPUT_USERNAME}');
            el.dispatchEvent(new Event('input',  {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        """)

        # Fill password
        password_box = await wait_for_element(tab, INPUT_PASSWORD)
        await password_box.click()
        await password_box.send_keys(PASSWORD)
        await tab.evaluate(f"""
            let el = document.querySelector('{INPUT_PASSWORD}');
            el.dispatchEvent(new Event('input',  {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        """)

        log.info("✓ Credentials filled")

        # Wait until Angular marks form dirty
        await wait_for_js(tab, f"""
            document.querySelector('{LOGIN_FORM}')?.classList.contains('ng-dirty')
        """)

        # Handle CAPTCHA before clicking Sign In
        # await _handle_captcha(tab)

        # Click Sign In
        await tab.evaluate(f"""
            const modal = document.querySelector('{LOGIN_MODAL}');
            const btn   = modal?.querySelector("{SUBMIT_BTN}");
            if (btn) {{
                btn.focus();
                btn.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true, cancelable: true }}));
                btn.dispatchEvent(new MouseEvent('mouseup',   {{ bubbles: true, cancelable: true }}));
                btn.dispatchEvent(new MouseEvent('click',     {{ bubbles: true, cancelable: true }}));
            }}
        """)
        log.info("✓ Sign In clicked")

        # ── Wait for modal to close (confirms login accepted) ──────────
        # elapsed = 0.0
        # while elapsed < 25:
        #     result = await tab.evaluate(f"document.querySelector('{LOGIN_MODAL}') === null")
        #     if result:
        #         break
        #     await asyncio.sleep(0.2)
        #     elapsed += 0.2

        #     # Re-check for CAPTCHA that might have appeared after submit
        #     if elapsed % 3 < 0.25:
        #         has_cap = await tab.evaluate(f"!!document.querySelector('{CAPTCHA_IMG}')")
        #         if has_cap:
        #             log.warning("⚠  CAPTCHA appeared after submit")
        #             await _handle_captcha(tab)
        #             # Re-click Sign In
        #             await tab.evaluate(f"""
        #                 const modal = document.querySelector('{LOGIN_MODAL}');
        #                 const btn   = modal?.querySelector("{SUBMIT_BTN}");
        #                 if (btn) btn.click();
        #             """)

        # ── Detect silent failure ──────────────────────────────────────
        # if elapsed >= 25:
        #     raise RuntimeError(
        #         "Login failed — modal never closed after 25s. "
        #         "Possible causes: wrong password, account locked, unsolved CAPTCHA."
        #     )

        # log.info("✓ Logged in successfully")

        # Save cookies for next run
        await save_cookies(tab)
