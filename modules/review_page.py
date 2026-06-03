# # import asyncio

# # from core.poller import wait_for_element
# # from core.logger import log


# # async def wait_for_user_captcha(tab):
# #     log.info("Waiting for captcha page...")

# #     await wait_for_element(tab, "#captcha")

# #     log.info("Please solve captcha and click Continue")

# #     while True:
# #         await asyncio.sleep(0.2)

# #         captcha_exists = await tab.evaluate(
# #             "document.querySelector('#captcha') !== null"
# #         )

# #         if not captcha_exists:
# #             log.info("Captcha submitted by user")
# #             return

# # captcha_filler.py

# import os
# import re
# import base64
# import asyncio
# import nodriver as uc
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# from core.poller import wait_for_element, wait_for_js
# from core.logger import log
# from core.profiler import timed

# load_dotenv()

# CAPTCHA_IMAGE = "img.captcha-img"
# CAPTCHA_INPUT = "#captcha"
# CONTINUE_BTN = "button.train_Search"
# REFRESH_BTN = ".glyphicon-repeat"

# MAX_CAPTCHA_ATTEMPTS = 3

# client = genai.Client(
#     api_key=os.getenv("API_KEY")
# )


# class CaptchaSolveFailed(Exception):
#     pass


# async def _type_char_by_char(tab, text: str):
#     for char in text:
#         await tab.send(
#             uc.cdp.input_.dispatch_key_event(
#                 type_="char",
#                 text=char
#             )
#         )
#         await asyncio.sleep(0.03)

# async def _get_captcha_base64(tab):

#     src = await tab.evaluate("""
#         (() => {
#             const img = document.querySelector('img.captcha-img');
#             return img ? img.src : null;
#         })()
#     """)

#     if not src:
#         raise Exception("Captcha image not found")

#     header, data = src.split(",", 1)

#     mime_type = (
#         header
#         .split(";")[0]
#         .replace("data:", "")
#     )

#     return data, mime_type


# async def _refresh_captcha(tab):
#     try:
#         btn = await tab.select(REFRESH_BTN)
#         if btn:
#             await btn.click()
#             await asyncio.sleep(1)
#             log.info("Captcha refreshed")
#     except Exception as e:
#         log.warning(f"Captcha refresh failed: {e}")


# # async def _fill_captcha(tab, text):

    

# #     captcha_box = await wait_for_element(
# #         tab,
# #         "#captcha"
# #     )

# #     await captcha_box.click()

# #     # Clear anything already present
# #     await tab.evaluate("""
# #         const el = document.querySelector('#captcha');
# #         if (el) {
# #             el.value = '';
# #         }
# #     """)

# #     # Type like a real user
# #     await captcha_box.send_keys(text)

# #     # Force Angular update
# #     await tab.evaluate("""
# #         const el = document.querySelector('#captcha');

# #         if (el) {
# #             el.dispatchEvent(
# #                 new Event('input', {
# #                     bubbles: true
# #                 })
# #             );

# #             el.dispatchEvent(
# #                 new Event('change', {
# #                     bubbles: true
# #                 })
# #             );

# #             el.dispatchEvent(
# #                 new Event('blur', {
# #                     bubbles: true
# #                 })
# #             );
# #         }
# #     """)
    
# #     value = await tab.evaluate("""
# #         document.querySelector('#captcha')?.value
# #     """)

# #     log.info(
# #         f"Captcha field contains: {value}"
# #     )


# #     log.info(
# #         f"Captcha entered: {text}"
# #     )

# async def _fill_captcha(tab, text):

#     captcha_box = await wait_for_element(
#         tab,
#         "#captcha"
#     )

#     await captcha_box.click()

#     await tab.evaluate("""
#         const el = document.querySelector('#captcha');
#         if (el) {
#             el.focus();
#             el.value = '';
#         }
#     """)

#     # Type exactly like passenger names
#     await _type_char_by_char(
#         tab,
#         text
#     )

#     value = await tab.evaluate("""
#         document.querySelector('#captcha')?.value
#     """)

#     log.info(
#         f"Captcha field contains: {value}"
#     )

#     if value != text:
#         log.warning(
#             f"Captcha mismatch. Expected={text} Got={value}"
#         )

#     log.info(
#         f"Captcha entered: {text}"
#     )


# async def solve_captcha_gemini(
#     base64_image,
#     mime_type="image/png"
# ):

#     image_bytes = base64.b64decode(base64_image)

#     for attempt in range(3):

#         try:

#             response = client.models.generate_content(
#                 model="gemini-2.5-flash",
#                 contents=[
#                     types.Part.from_text(
#                         text="""
# Read this captcha.

# Return the captcha EXACTLY as shown.

# Rules:
# - Preserve uppercase letters
# - Preserve lowercase letters
# - Preserve symbols
# - Preserve numbers
# - Do not change case
# - Do not explain
# - Return only the captcha text
# """
#                     ),
#                     types.Part.from_bytes(
#                         data=image_bytes,
#                         mime_type=mime_type
#                     )
#                 ]
#             )

#             # text = response.text.strip().upper()
#             text = response.text.strip()

#             # text = re.sub(
#             #     r'[^A-Z0-9]',
#             #     '',
#             #     text
#             # )
#             text = text.strip()

#             text = text.replace('"', '')
#             text = text.replace("'", '')
#             text = text.replace(" ", '')
#             text = text.replace("\n", '')

#             if len(text) >= 4:
#                 return text

#         except Exception as e:

#             log.warning(
#                 f"Gemini solve attempt {attempt+1} failed: {e}"
#             )

#         await asyncio.sleep(0.5)

#     raise CaptchaSolveFailed(
#         "Gemini failed to solve captcha"
#     )

# # async def _click_continue(tab):
# #     btn = await wait_for_element(tab, CONTINUE_BTN)

# #     try:
# #         await btn.click()
# #     except:
# #         await btn.mouse_click()

# #     log.info("Continue clicked")

# async def _click_continue(tab):

#     await wait_for_element(
#         tab,
#         CONTINUE_BTN
#     )

#     await tab.evaluate("""
#         (() => {
#             const btn =
#                 document.querySelector(
#                     'button.train_Search'
#                 );

#             if (btn) {
#                 btn.click();
#             }
#         })()
#     """)

#     log.info("Continue clicked")


# async def _captcha_page_gone(tab):
#     try:
#         return await tab.evaluate("""
#             !document.querySelector('img.captcha-img')
#         """)
#     except:
#         return False


# async def fill_captcha_page(tab):

#     async with timed("captcha_filler"):

#         log.info("Waiting for captcha page")

#         await wait_for_element(
#             tab,
#             CAPTCHA_IMAGE,
#             timeout=15
#         )

#         for attempt in range(MAX_CAPTCHA_ATTEMPTS):

#             log.info(
#                 f"Captcha attempt {attempt+1}/{MAX_CAPTCHA_ATTEMPTS}"
#             )

#             try:

#                 # captcha_b64 = await _get_captcha_base64(tab)

#                 # solution = await solve_captcha_gemini(
#                 #     captcha_b64
#                 # )
#                 captcha_b64, mime_type = await _get_captcha_base64(tab)

#                 solution = await solve_captcha_gemini(
#                     captcha_b64,
#                     mime_type
# )

#                 log.info(
#                     f"Gemini solved captcha: {solution}"
#                 )

#                 await _fill_captcha(
#                     tab,
#                     solution
#                 )
#                 value = await tab.evaluate("""
#                 document.querySelector('#captcha')?.value
#                 """)

#                 log.info(
#                     f"FINAL CAPTCHA FIELD VALUE: {value}"
#                 )

#                 await _click_continue(tab)

#                 try:
#                     await asyncio.wait_for(
#                         wait_for_js(
#                             tab,
#                             "document.querySelector('img.captcha-img') === null"
#                         ),
#                         timeout=8
#                     )

#                     log.info(
#                         "Captcha accepted"
#                     )

#                     return

#                 except asyncio.TimeoutError:

#                     log.warning(
#                         "Still on captcha page"
#                     )

#             except Exception as e:

#                 log.warning(
#                     f"Captcha attempt failed: {e}"
#                 )

#             if attempt < MAX_CAPTCHA_ATTEMPTS - 1:
#                 await _refresh_captcha(tab)

#         raise CaptchaSolveFailed(
#             "All captcha attempts failed"
#         )
# import asyncio

# from core.poller import wait_for_element
# from core.logger import log


# async def wait_for_user_captcha(tab):
#     log.info("Waiting for captcha page...")

#     await wait_for_element(tab, "#captcha")

#     log.info("Please solve captcha and click Continue")

#     while True:
#         await asyncio.sleep(0.2)

#         captcha_exists = await tab.evaluate(
#             "document.querySelector('#captcha') !== null"
#         )

#         if not captcha_exists:
#             log.info("Captcha submitted by user")
#             return

# captcha_filler.py

import os
import re
import base64
import asyncio
import nodriver as uc
from dotenv import load_dotenv
from google import genai
from google.genai import types

from core.poller import wait_for_element, wait_for_js
from core.logger import log
from core.profiler import timed

load_dotenv()

CAPTCHA_IMAGE = "img.captcha-img"
CAPTCHA_INPUT = "#captcha"
CONTINUE_BTN = "button.train_Search"
REFRESH_BTN = ".glyphicon-repeat"

MAX_CAPTCHA_ATTEMPTS = 3

client = genai.Client(
    api_key=os.getenv("API_KEY")
)


class CaptchaSolveFailed(Exception):
    pass


async def _type_char_by_char(tab, text: str):
    for char in text:
        await tab.send(
            uc.cdp.input_.dispatch_key_event(
                type_="char",
                text=char
            )
        )
        await asyncio.sleep(0.03)

async def _get_captcha_base64(tab):

    src = await tab.evaluate("""
        (() => {
            const img = document.querySelector('img.captcha-img');
            return img ? img.src : null;
        })()
    """)

    if not src:
        raise Exception("Captcha image not found")

    header, data = src.split(",", 1)

    mime_type = (
        header
        .split(";")[0]
        .replace("data:", "")
    )

    return data, mime_type


async def _refresh_captcha(tab):
    try:
        btn = await tab.select(REFRESH_BTN)
        if btn:
            await btn.click()
            await asyncio.sleep(1)
            log.info("Captcha refreshed")
    except Exception as e:
        log.warning(f"Captcha refresh failed: {e}")


# async def _fill_captcha(tab, text):

    

#     captcha_box = await wait_for_element(
#         tab,
#         "#captcha"
#     )

#     await captcha_box.click()

#     # Clear anything already present
#     await tab.evaluate("""
#         const el = document.querySelector('#captcha');
#         if (el) {
#             el.value = '';
#         }
#     """)

#     # Type like a real user
#     await captcha_box.send_keys(text)

#     # Force Angular update
#     await tab.evaluate("""
#         const el = document.querySelector('#captcha');

#         if (el) {
#             el.dispatchEvent(
#                 new Event('input', {
#                     bubbles: true
#                 })
#             );

#             el.dispatchEvent(
#                 new Event('change', {
#                     bubbles: true
#                 })
#             );

#             el.dispatchEvent(
#                 new Event('blur', {
#                     bubbles: true
#                 })
#             );
#         }
#     """)
    
#     value = await tab.evaluate("""
#         document.querySelector('#captcha')?.value
#     """)

#     log.info(
#         f"Captcha field contains: {value}"
#     )


#     log.info(
#         f"Captcha entered: {text}"
#     )

async def _fill_captcha(tab, text):

    captcha_box = await wait_for_element(
        tab,
        "#captcha"
    )

    await captcha_box.click()

    await tab.evaluate("""
        const el = document.querySelector('#captcha');
        if (el) {
            el.focus();
            el.value = '';
        }
    """)

    # Type exactly like passenger names
    await _type_char_by_char(
        tab,
        text
    )

    value = await tab.evaluate("""
        document.querySelector('#captcha')?.value
    """)

    log.info(
        f"Captcha field contains: {value}"
    )

    if value != text:
        log.warning(
            f"Captcha mismatch. Expected={text} Got={value}"
        )

    log.info(
        f"Captcha entered: {text}"
    )


async def solve_captcha_gemini(
    base64_image,
    mime_type="image/png"
):

    image_bytes = base64.b64decode(base64_image)

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_text(
                        text="""
Read this captcha.

Return the captcha EXACTLY as shown.

Rules:
- Preserve uppercase letters
- Preserve lowercase letters
- Preserve symbols
- Preserve numbers
- Do not change case
- Do not explain
- Return only the captcha text
"""
                    ),
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=mime_type
                    )
                ]
            )

            # text = response.text.strip().upper()
            text = response.text.strip()

            # text = re.sub(
            #     r'[^A-Z0-9]',
            #     '',
            #     text
            # )
            text = text.strip()

            text = text.replace('"', '')
            text = text.replace("'", '')
            text = text.replace(" ", '')
            text = text.replace("\n", '')

            if len(text) >= 4:
                return text

        except Exception as e:

            log.warning(
                f"Gemini solve attempt {attempt+1} failed: {e}"
            )

        await asyncio.sleep(0.5)

    raise CaptchaSolveFailed(
        "Gemini failed to solve captcha"
    )

# async def _click_continue(tab):
#     btn = await wait_for_element(tab, CONTINUE_BTN)

#     try:
#         await btn.click()
#     except:
#         await btn.mouse_click()

#     log.info("Continue clicked")

async def _click_continue(tab):

    await wait_for_element(
        tab,
        CONTINUE_BTN
    )

    await tab.evaluate("""
        (() => {
            const btn =
                document.querySelector(
                    'button.train_Search'
                );

            if (btn) {
                btn.click();
            }
        })()
    """)

    log.info("Continue clicked")


async def _captcha_page_gone(tab):
    try:
        return await tab.evaluate("""
            !document.querySelector('img.captcha-img')
        """)
    except:
        return False


async def fill_captcha_page(tab):

    async with timed("captcha_filler"):

        log.info("Waiting for captcha page")

        await wait_for_element(
            tab,
            CAPTCHA_IMAGE,
            timeout=15
        )

        for attempt in range(MAX_CAPTCHA_ATTEMPTS):

            log.info(
                f"Captcha attempt {attempt+1}/{MAX_CAPTCHA_ATTEMPTS}"
            )

            try:

                # captcha_b64 = await _get_captcha_base64(tab)

                # solution = await solve_captcha_gemini(
                #     captcha_b64
                # )
                captcha_b64, mime_type = await _get_captcha_base64(tab)

                solution = await solve_captcha_gemini(
                    captcha_b64,
                    mime_type
)

                log.info(
                    f"Gemini solved captcha: {solution}"
                )

                await _fill_captcha(
                    tab,
                    solution
                )
                value = await tab.evaluate("""
                document.querySelector('#captcha')?.value
                """)

                log.info(
                    f"FINAL CAPTCHA FIELD VALUE: {value}"
                )

                await _click_continue(tab)

                try:
                    await asyncio.wait_for(
                        wait_for_js(
                            tab,
                            "document.querySelector('img.captcha-img') === null"
                        ),
                        timeout=8
                    )

                    log.info(
                        "Captcha accepted"
                    )

                    return

                except asyncio.TimeoutError:

                    log.warning(
                        "Still on captcha page"
                    )

            except Exception as e:

                log.warning(
                    f"Captcha attempt failed: {e}"
                )

            if attempt < MAX_CAPTCHA_ATTEMPTS - 1:
                await _refresh_captcha(tab)

        raise CaptchaSolveFailed(
            "All captcha attempts failed"
        )