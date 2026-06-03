# import json
# import os
# import telebot
# import sys
# from dotenv import load_dotenv
# from pathlib import Path
# from datetime import datetime
# import traceback
# from flask import Flask
# import threading

# app = Flask(__name__)
# @app.route("/")
# def root():
#     return "😼 billa is alive", 200

# @app.route("/health")
# def health():
#     return "😼 billa is alive", 200

# def run_health_server():
#     app.run(host="0.0.0.0", port=8080)


# load_dotenv()
# BASE_DIR = Path(__file__).resolve().parent.parent

# ROUTES_FILE = BASE_DIR / "config" / "routes.json"
# PASSENGERS_FILE = BASE_DIR / "config" / "passengers.json"

# START_TIME = datetime.now()

# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# OWNER_ID = int(os.getenv("TELEGRAM_OWNER_ID", "0"))

# bot = telebot.TeleBot(BOT_TOKEN)


# # --------------------------------------------------
# # Security
# # --------------------------------------------------

# def owner_only(message):
#     return message.from_user.id == OWNER_ID


# def unauthorized(message):
#     bot.reply_to(
#         message,
#         "🚫 bro who are you 💀\nbilla ke area se door reh fr fr 😼🔫\n\nnot ur bot bestie."
#     )


# # --------------------------------------------------
# # Helpers
# # --------------------------------------------------

# def load_routes():
#     try:
#         with open(ROUTES_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception as e:
#         raise RuntimeError(f"routes.json error: {e}")


# def load_passengers():
#     try:
#         with open(PASSENGERS_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception as e:
#         raise RuntimeError(f"passengers.json error: {e}")


# def get_uptime():
#     delta = datetime.now() - START_TIME
#     days = delta.days
#     hours = delta.seconds // 3600
#     mins = (delta.seconds % 3600) // 60
#     return f"{days}d {hours}h {mins}m"


# # --------------------------------------------------
# # Commands
# # --------------------------------------------------

# @bot.message_handler(commands=["restart"])
# def restart_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     bot.reply_to(
#         message,
#         "🔄 billa punarjanam le raha hai... ong 💀\n\n"
#         "if running under Render/VPS supervisor, billa will respawn no cap 😼"
#     )


# @bot.message_handler(commands=["logs"])
# def logs_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     try:
#         with open("logs/billa.log", "r", encoding="utf-8") as f:
#             lines = f.readlines()[-20:]

#         bot.reply_to(
#             message,
#             "📜 last 10 logs (yikes edition):\n\n" + "".join(lines[-10:])
#         )

#     except Exception as e:
#         bot.reply_to(message, f"❌ log moment:\n{e}")


# @bot.message_handler(commands=["start"])
# def start_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     text = (
#         "😼🔫 BADMOSH BILLA — ONLINE AND SENDING\n\n"
#         "tatkal control center has entered the chat fr\n\n"
#         "━━━━━━━━━━━━━━━\n"
#         "📊 THE DASHBOARD\n"
#         "━━━━━━━━━━━━━━━\n"
#         "👀 /status  — vibe check\n"
#         "⚙️ /settings  — all the deets\n"
#         "🟢 /health  — is billa okay?\n\n"
#         "━━━━━━━━━━━━━━━\n"
#         "🚂 TRAIN STUFF\n"
#         "━━━━━━━━━━━━━━━\n"
#         "🚆 /trains  — train list\n"
#         "👥 /passengers  — squad\n\n"
#         "━━━━━━━━━━━━━━━\n"
#         "📖 /help  — full command list\n"
#         "━━━━━━━━━━━━━━━\n\n"
#         "🤖 ready to cook boss. no cap.\n\n"
#         "🔫 phew phew"
#     )
#     bot.reply_to(message, text)


# @bot.message_handler(commands=["help"])
# def help_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     bot.reply_to(
#         message,
#         "😼🔫 BADMOSH BILLA — COMMAND DROP\n\n"
#         "━━━━━━━━━━━━━━━\n"
#         "📊 VIBE CHECKS\n"
#         "━━━━━━━━━━━━━━━\n"
#         "👀 /status  — full status lowdown\n"
#         "⚙️ /settings  — current config\n"
#         "🟢 /health  — health check\n"
#         "💓 /ping  — billa alive?\n\n"
#         "━━━━━━━━━━━━━━━\n"
#         "🚂 BOOKING INTEL\n"
#         "━━━━━━━━━━━━━━━\n"
#         "🚆 /trains  — train list\n"
#         "👥 /passengers  — squad list\n"
#         "📅 /date  — journey date\n"
#         "🎫 /quota  — quota type\n"
#         "⏰ /firetime  — when to fire\n"
#         "💳 /payment  — payment method\n\n"
#         "━━━━━━━━━━━━━━━\n"
#         "😼 BILLA ZONE\n"
#         "━━━━━━━━━━━━━━━\n"
#         "😺 /about  — origin story\n"
#         "📜 /logs  — last logs\n"
#         "🔄 /restart  — reincarnation\n"
#         "🥛 /donate  — fuel the cat\n\n"
#         "━━━━━━━━━━━━━━━\n\n"
#         "🤖 status: online\n"
#         "🔒 access: owner only (except /donate, that's public bestie)\n"
#         "🚂 mode: tatkal ready\n\n"
#         "🔫 phew phew boss!"
#     )


# @bot.message_handler(commands=["ping"])
# def ping_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     bot.reply_to(
#         message,
#         f"😼 billa zinda hai and thriving boss!\n\n"
#         f"⏱ uptime: {get_uptime()}\n\n"
#         f"not a single ded 🔫 phew phew"
#     )


# @bot.message_handler(commands=["status"])
# def status_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     try:
#         route = load_routes()
#         pax = load_passengers()

#         text = (
#             "📊 BILLA STATUS REPORT\n\n"
#             f"🤖 bot: online and eating\n"
#             f"⏱ uptime: {get_uptime()}\n\n"
#             "━━━━━━━━━━━━━━━\n"
#             f"🚂 route: {route['from_station']} → {route['to_station']}\n"
#             f"📅 date: {route['journey_date']}\n"
#             f"🎫 quota: {route['quota']}\n"
#             f"👥 passengers: {len(pax['passengers'])} homies\n"
#             f"🔥 fire time: {route['fire_time']}\n"
#             f"💳 payment: {route['payment']['method']}\n"
#             "━━━━━━━━━━━━━━━\n\n"
#             "all good no cap ✅"
#         )

#         bot.reply_to(message, text)

#     except Exception as e:
#         bot.reply_to(message, f"❌ status flopped rn\n\n{e}")


# @bot.message_handler(commands=["settings"])
# def settings_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     try:
#         route = load_routes()
#         pax = load_passengers()

#         trains = "\n".join(
#             f"  🚆 {t['number']} → {', '.join(t['classes'])}"
#             for t in route["trains"]
#         )

#         passengers = "\n".join(
#             f"  👤 {p['name']}"
#             for p in pax["passengers"]
#         )

#         text = (
#             "⚙️ CURRENT SETTINGS (spilling the config)\n\n"
#             "━━━━━━━━━━━━━━━\n"
#             f"🚂 route: {route['from_station']} → {route['to_station']}\n"
#             f"📅 date: {route['journey_date']}\n"
#             f"🎫 quota: {route['quota']}\n"
#             f"🔥 fire time: {route['fire_time']}\n"
#             f"💳 payment: {route['payment']['method']}\n\n"
#             "🚆 trains:\n"
#             f"{trains}\n\n"
#             "👥 passengers:\n"
#             f"{passengers}\n"
#             "━━━━━━━━━━━━━━━\n\n"
#             "that's the full tea ☕"
#         )

#         bot.reply_to(message, text)

#     except Exception as e:
#         bot.reply_to(message, f"❌ settings said nah\n\n{e}")


# @bot.message_handler(commands=["health"])
# def health_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     try:
#         load_routes()
#         load_passengers()

#         bot.reply_to(
#             message,
#             "🟢 HEALTH CHECK — billa is eating good\n\n"
#             "🤖 telegram bot: ✅ slay\n"
#             "📂 routes.json: ✅ valid\n"
#             "👥 passengers.json: ✅ loaded\n"
#             "🔒 owner auth: ✅ locked in\n\n"
#             "everything bussin no cap 😼\n"
#             "🔫 phew phew"
#         )

#     except Exception as e:
#         bot.reply_to(
#             message,
#             f"🔴 health check flopped bestie\n\n{e}"
#         )


# @bot.message_handler(commands=["trains"])
# def trains_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     route = load_routes()

#     lines = ["🚆 BILLA'S TRAIN LIST (the lineup)\n"]

#     for train in route["trains"]:
#         classes = ", ".join(train["classes"])
#         lines.append(f"🚂 {train['number']} → {classes}")

#     lines.append("\nthat's the roster fr 🔥")
#     bot.reply_to(message, "\n".join(lines))


# @bot.message_handler(commands=["passengers"])
# def passengers_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     pax = load_passengers()

#     lines = ["👥 THE BILLA GANG (squad goals)\n"]

#     for p in pax["passengers"]:
#         lines.append(f"• {p['name']}")

#     lines.append("\nall seated (hopefully) 🙏")
#     bot.reply_to(message, "\n".join(lines))


# @bot.message_handler(commands=["date"])
# def date_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     route = load_routes()

#     bot.reply_to(
#         message,
#         f"📅 journey date:\n\n{route['journey_date']}\n\nmark ur calendar bestie 🗓️"
#     )


# @bot.message_handler(commands=["quota"])
# def quota_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     route = load_routes()

#     bot.reply_to(
#         message,
#         f"🎫 quota type:\n\n{route['quota']}\n\nwe locked in 🔒"
#     )


# @bot.message_handler(commands=["firetime"])
# def firetime_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     route = load_routes()

#     bot.reply_to(
#         message,
#         f"⏰ fire time:\n\n{route['fire_time']}\n\ndon't be late or it's a L 💀"
#     )


# @bot.message_handler(commands=["payment"])
# def payment_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     route = load_routes()

#     bot.reply_to(
#         message,
#         f"💳 payment method:\n\n{route['payment']['method']}\n\nmoney ready? bet. 💰"
#     )


# @bot.message_handler(commands=["about"])
# def about_cmd(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     bot.reply_to(
#         message,
#         "😼 BADMOSH BILLA — THE ORIGIN STORY\n\n"
#         "🚂 tatkal control center\n"
#         "🤖 ur fav telegram automation bestie\n\n"
#         "version: 1.0.0 (era one)\n\n"
#         "━━━━━━━━━━━━━━━\n"
#         "what billa does:\n"
#         "• monitors tatkal like a hawk 🦅\n"
#         "• tracks passengers no cap\n"
#         "• watches trains (literally)\n"
#         "• booking control — coming soon™️\n"
#         "━━━━━━━━━━━━━━━\n\n"
#         "got the seat? 🔥 billa ate fr\n"
#         "no seat? 😤 irctc ki galti bestie, not billa's.\n\n"
#         "made with 🥛 for boss sumit 😼\n\n"
#         "🔫 phew phew"
#     )


# # ✅ PUBLIC — no owner_only check
# @bot.message_handler(commands=["donate"])
# def donate_cmd(message):
#     caption = (
#         "🥛 DONATE TO THE BADMOSH BILLA FUND\n\n"
#         "billa runs on:\n"
#         "☕ coffee\n"
#         "🥛 milk (obviously)\n"
#         "🍗 chicken\n"
#         "🚂 tatkal experiments (expensive fr)\n\n"
#         "━━━━━━━━━━━━━━━\n"
#         "upi: yourupi@oksbi\n"
#         "━━━━━━━━━━━━━━━\n\n"
#         "every rupee makes billa faster 😼\n"
#         "no pressure but also... please 🙏\n\n"
#         "🔫 phew phew"
#     )

#     try:
#         with open("assets/donate_qr.jpg", "rb") as qr:
#             bot.send_photo(
#                 message.chat.id,
#                 qr,
#                 caption=caption
#             )
#     except FileNotFoundError:
#         bot.reply_to(message, caption + "\n\n(qr code not set up yet bestie 😭)")


# # --------------------------------------------------
# # Catch-all
# # --------------------------------------------------

# @bot.message_handler(func=lambda m: True)
# def unknown(message):
#     if not owner_only(message):
#         return unauthorized(message)

#     bot.reply_to(
#         message,
#         "🤨 bro what even is this command 💀\n\nbilla said huh.\n\ntry /help bestie"
#     )


# # --------------------------------------------------
# # Start
# # --------------------------------------------------

# if __name__ == "__main__":
#     print("😼 Badmosh Billa Online... no cap")
#     threading.Thread(target=run_health_server, daemon=True).start()

#     while True:
#         try:
#             bot.infinity_polling(
#                 skip_pending=True,
#                 timeout=30,
#                 long_polling_timeout=30
#             )

#         except Exception:
#             print(traceback.format_exc())

#             import time
#             time.sleep(5)

import json
import os
import requests
import telebot
import sys
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import traceback
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def root():
    return "😼 billa is alive", 200

@app.route("/health")
def health():
    return "😼 billa is alive", 200

def run_health_server():
    app.run(host="0.0.0.0", port=8080)


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

ROUTES_FILE = BASE_DIR / "config" / "routes.json"
PASSENGERS_FILE = BASE_DIR / "config" / "passengers.json"

START_TIME = datetime.now()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = int(os.getenv("TELEGRAM_OWNER_ID", "0"))

bot = telebot.TeleBot(BOT_TOKEN)

# --------------------------------------------------
# RapidAPI / IRCTC Config
# --------------------------------------------------

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "irctc1.p.rapidapi.com"
RAPIDAPI_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
}
IRCTC_BASE_URL = "https://irctc1.p.rapidapi.com/api/v3"


# --------------------------------------------------
# RapidAPI Helper Functions
# --------------------------------------------------

def api_search_trains(from_station: str, to_station: str, date: str) -> dict:
    url = f"{IRCTC_BASE_URL}/trainBetweenStations"
    params = {
        "fromStationCode": from_station.upper(),
        "toStationCode": to_station.upper(),
        "dateOfJourney": date,
    }
    resp = requests.get(url, headers=RAPIDAPI_HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_seat_availability(from_station: str, to_station: str, date: str) -> dict:
    url = f"{IRCTC_BASE_URL}/getAvailabilityCalendar"
    params = {
        "fromStationCode": from_station.upper(),
        "toStationCode": to_station.upper(),
        "dateOfJourney": date,
    }
    resp = requests.get(url, headers=RAPIDAPI_HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_live_train(train_no: str) -> dict:
    url = f"{IRCTC_BASE_URL}/liveTrainStatus"
    params = {"trainNo": train_no, "startDay": "1"}
    resp = requests.get(url, headers=RAPIDAPI_HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_pnr_status(pnr: str) -> dict:
    url = f"{IRCTC_BASE_URL}/getPNRStatus"
    params = {"pnrNumber": pnr}
    resp = requests.get(url, headers=RAPIDAPI_HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_fetch_seat_avail(train_no: str, source: str, destination: str,
                         date: str, travel_class: str, quota: str) -> dict:
    url = f"{IRCTC_BASE_URL}/checkSeatAvailability"
    params = {
        "classType": travel_class.upper(),
        "fromStationCode": source.upper(),
        "quota": quota.upper(),
        "toStationCode": destination.upper(),
        "trainNo": train_no,
        "date": date,
    }
    resp = requests.get(url, headers=RAPIDAPI_HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


# --------------------------------------------------
# Security
# --------------------------------------------------

def owner_only(message):
    return message.from_user.id == OWNER_ID


def unauthorized(message):
    bot.reply_to(
        message,
        "🚫 bro who are you 💀\nbilla ke area se door reh fr fr 😼🔫\n\nnot ur bot bestie."
    )


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def load_routes():
    try:
        with open(ROUTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"routes.json error: {e}")


def load_passengers():
    try:
        with open(PASSENGERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"passengers.json error: {e}")


def get_uptime():
    delta = datetime.now() - START_TIME
    days = delta.days
    hours = delta.seconds // 3600
    mins = (delta.seconds % 3600) // 60
    return f"{days}d {hours}h {mins}m"


# --------------------------------------------------
# Owner Commands
# --------------------------------------------------

@bot.message_handler(commands=["restart"])
def restart_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    bot.reply_to(
        message,
        "🔄 billa punarjanam le raha hai... ong 💀\n\n"
        "if running under Render/VPS supervisor, billa will respawn no cap 😼"
    )


@bot.message_handler(commands=["logs"])
def logs_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    try:
        with open("logs/billa.log", "r", encoding="utf-8") as f:
            lines = f.readlines()[-20:]

        bot.reply_to(
            message,
            "📜 last 10 logs (yikes edition):\n\n" + "".join(lines[-10:])
        )

    except Exception as e:
        bot.reply_to(message, f"❌ log moment:\n{e}")


@bot.message_handler(commands=["start"])
def start_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    text = (
        "😼🔫 BADMOSH BILLA — ONLINE AND SENDING\n\n"
        "tatkal control center has entered the chat fr\n\n"
        "━━━━━━━━━━━━━━━\n"
        "📊 THE DASHBOARD\n"
        "━━━━━━━━━━━━━━━\n"
        "👀 /status  — vibe check\n"
        "⚙️ /settings  — all the deets\n"
        "🟢 /health  — is billa okay?\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🚂 TRAIN STUFF\n"
        "━━━━━━━━━━━━━━━\n"
        "🚆 /trains  — train list\n"
        "👥 /passengers  — squad\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🔍 IRCTC LOOKUP (public)\n"
        "━━━━━━━━━━━━━━━\n"
        "🔎 /searchtrains  — find trains\n"
        "🎫 /availability  — seat availability\n"
        "📡 /livetrain  — live status\n"
        "🎟️ /pnr  — pnr status\n"
        "💺 /seatavail  — detailed seat check\n\n"
        "━━━━━━━━━━━━━━━\n"
        "📖 /help  — full command list\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🤖 ready to cook boss. no cap.\n\n"
        "🔫 phew phew"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["help"])
def help_cmd(message):
    if not owner_only(message):
        # public users get IRCTC commands help only
        bot.reply_to(
            message,
            "😼 BILLA — PUBLIC COMMANDS\n\n"
            "━━━━━━━━━━━━━━━\n"
            "🔍 IRCTC LOOKUP\n"
            "━━━━━━━━━━━━━━━\n"
            "🔎 /searchtrains <FROM> <TO> <YYYYMMDD>\n"
            "🎫 /availability <FROM> <TO> <YYYYMMDD>\n"
            "📡 /livetrain <TRAIN_NO>\n"
            "🎟️ /pnr <PNR_NO>\n"
            "💺 /seatavail <trainNo> <src> <dst> <date> <class> <quota>\n\n"
            "━━━━━━━━━━━━━━━\n"
            "Example: `/searchtrains NDLS BCT 20250810`\n"
            "━━━━━━━━━━━━━━━\n\n"
            "🔫 phew phew",
            parse_mode="Markdown"
        )
        return

    bot.reply_to(
        message,
        "😼🔫 BADMOSH BILLA — COMMAND DROP\n\n"
        "━━━━━━━━━━━━━━━\n"
        "📊 VIBE CHECKS (owner)\n"
        "━━━━━━━━━━━━━━━\n"
        "👀 /status  — full status lowdown\n"
        "⚙️ /settings  — current config\n"
        "🟢 /health  — health check\n"
        "💓 /ping  — billa alive?\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🚂 BOOKING INTEL (owner)\n"
        "━━━━━━━━━━━━━━━\n"
        "🚆 /trains  — train list\n"
        "👥 /passengers  — squad list\n"
        "📅 /date  — journey date\n"
        "🎫 /quota  — quota type\n"
        "⏰ /firetime  — when to fire\n"
        "💳 /payment  — payment method\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🔍 IRCTC LOOKUP (public)\n"
        "━━━━━━━━━━━━━━━\n"
        "🔎 /searchtrains <FROM> <TO> <YYYYMMDD>\n"
        "🎫 /availability <FROM> <TO> <YYYYMMDD>\n"
        "📡 /livetrain <TRAIN_NO>\n"
        "🎟️ /pnr <PNR_NO>\n"
        "💺 /seatavail <trainNo> <src> <dst> <date> <class> <quota>\n\n"
        "━━━━━━━━━━━━━━━\n"
        "😼 BILLA ZONE (owner)\n"
        "━━━━━━━━━━━━━━━\n"
        "😺 /about  — origin story\n"
        "📜 /logs  — last logs\n"
        "🔄 /restart  — reincarnation\n"
        "🥛 /donate  — fuel the cat\n\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🤖 status: online\n"
        "🔒 owner commands: locked\n"
        "🌐 IRCTC commands: public\n\n"
        "🔫 phew phew boss!",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=["ping"])
def ping_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    bot.reply_to(
        message,
        f"😼 billa zinda hai and thriving boss!\n\n"
        f"⏱ uptime: {get_uptime()}\n\n"
        f"not a single ded 🔫 phew phew"
    )


@bot.message_handler(commands=["status"])
def status_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    try:
        route = load_routes()
        pax = load_passengers()

        text = (
            "📊 BILLA STATUS REPORT\n\n"
            f"🤖 bot: online and eating\n"
            f"⏱ uptime: {get_uptime()}\n\n"
            "━━━━━━━━━━━━━━━\n"
            f"🚂 route: {route['from_station']} → {route['to_station']}\n"
            f"📅 date: {route['journey_date']}\n"
            f"🎫 quota: {route['quota']}\n"
            f"👥 passengers: {len(pax['passengers'])} homies\n"
            f"🔥 fire time: {route['fire_time']}\n"
            f"💳 payment: {route['payment']['method']}\n"
            "━━━━━━━━━━━━━━━\n\n"
            "all good no cap ✅"
        )

        bot.reply_to(message, text)

    except Exception as e:
        bot.reply_to(message, f"❌ status flopped rn\n\n{e}")


@bot.message_handler(commands=["settings"])
def settings_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    try:
        route = load_routes()
        pax = load_passengers()

        trains = "\n".join(
            f"  🚆 {t['number']} → {', '.join(t['classes'])}"
            for t in route["trains"]
        )

        passengers = "\n".join(
            f"  👤 {p['name']}"
            for p in pax["passengers"]
        )

        text = (
            "⚙️ CURRENT SETTINGS (spilling the config)\n\n"
            "━━━━━━━━━━━━━━━\n"
            f"🚂 route: {route['from_station']} → {route['to_station']}\n"
            f"📅 date: {route['journey_date']}\n"
            f"🎫 quota: {route['quota']}\n"
            f"🔥 fire time: {route['fire_time']}\n"
            f"💳 payment: {route['payment']['method']}\n\n"
            "🚆 trains:\n"
            f"{trains}\n\n"
            "👥 passengers:\n"
            f"{passengers}\n"
            "━━━━━━━━━━━━━━━\n\n"
            "that's the full tea ☕"
        )

        bot.reply_to(message, text)

    except Exception as e:
        bot.reply_to(message, f"❌ settings said nah\n\n{e}")


@bot.message_handler(commands=["health"])
def health_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    try:
        load_routes()
        load_passengers()

        bot.reply_to(
            message,
            "🟢 HEALTH CHECK — billa is eating good\n\n"
            "🤖 telegram bot: ✅ slay\n"
            "📂 routes.json: ✅ valid\n"
            "👥 passengers.json: ✅ loaded\n"
            "🔒 owner auth: ✅ locked in\n\n"
            "everything bussin no cap 😼\n"
            "🔫 phew phew"
        )

    except Exception as e:
        bot.reply_to(
            message,
            f"🔴 health check flopped bestie\n\n{e}"
        )


@bot.message_handler(commands=["trains"])
def trains_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    route = load_routes()

    lines = ["🚆 BILLA'S TRAIN LIST (the lineup)\n"]

    for train in route["trains"]:
        classes = ", ".join(train["classes"])
        lines.append(f"🚂 {train['number']} → {classes}")

    lines.append("\nthat's the roster fr 🔥")
    bot.reply_to(message, "\n".join(lines))


@bot.message_handler(commands=["passengers"])
def passengers_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    pax = load_passengers()

    lines = ["👥 THE BILLA GANG (squad goals)\n"]

    for p in pax["passengers"]:
        lines.append(f"• {p['name']}")

    lines.append("\nall seated (hopefully) 🙏")
    bot.reply_to(message, "\n".join(lines))


@bot.message_handler(commands=["date"])
def date_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    route = load_routes()

    bot.reply_to(
        message,
        f"📅 journey date:\n\n{route['journey_date']}\n\nmark ur calendar bestie 🗓️"
    )


@bot.message_handler(commands=["quota"])
def quota_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    route = load_routes()

    bot.reply_to(
        message,
        f"🎫 quota type:\n\n{route['quota']}\n\nwe locked in 🔒"
    )


@bot.message_handler(commands=["firetime"])
def firetime_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    route = load_routes()

    bot.reply_to(
        message,
        f"⏰ fire time:\n\n{route['fire_time']}\n\ndon't be late or it's a L 💀"
    )


@bot.message_handler(commands=["payment"])
def payment_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    route = load_routes()

    bot.reply_to(
        message,
        f"💳 payment method:\n\n{route['payment']['method']}\n\nmoney ready? bet. 💰"
    )


@bot.message_handler(commands=["about"])
def about_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    bot.reply_to(
        message,
        "😼 BADMOSH BILLA — THE ORIGIN STORY\n\n"
        "🚂 tatkal control center\n"
        "🤖 ur fav telegram automation bestie\n\n"
        "version: 1.0.0 (era one)\n\n"
        "━━━━━━━━━━━━━━━\n"
        "what billa does:\n"
        "• monitors tatkal like a hawk 🦅\n"
        "• tracks passengers no cap\n"
        "• watches trains (literally)\n"
        "• booking control — coming soon™️\n"
        "━━━━━━━━━━━━━━━\n\n"
        "got the seat? 🔥 billa ate fr\n"
        "no seat? 😤 irctc ki galti bestie, not billa's.\n\n"
        "made with 🥛 for boss sumit 😼\n\n"
        "🔫 phew phew"
    )


# ✅ PUBLIC — no owner_only check
@bot.message_handler(commands=["donate"])
def donate_cmd(message):
    caption = (
        "🥛 DONATE TO THE BADMOSH BILLA FUND\n\n"
        "billa runs on:\n"
        "☕ coffee\n"
        "🥛 milk (obviously)\n"
        "🍗 chicken\n"
        "🚂 tatkal experiments (expensive fr)\n\n"
        "━━━━━━━━━━━━━━━\n"
        "upi: yourupi@oksbi\n"
        "━━━━━━━━━━━━━━━\n\n"
        "every rupee makes billa faster 😼\n"
        "no pressure but also... please 🙏\n\n"
        "🔫 phew phew"
    )

    try:
        with open("assets/donate_qr.jpg", "rb") as qr:
            bot.send_photo(
                message.chat.id,
                qr,
                caption=caption
            )
    except FileNotFoundError:
        bot.reply_to(message, caption + "\n\n(qr code not set up yet bestie 😭)")


# --------------------------------------------------
# PUBLIC IRCTC Commands (anyone can use these)
# --------------------------------------------------

@bot.message_handler(commands=["searchtrains"])
def searchtrains_cmd(message):
    """Usage: /searchtrains <FROM> <TO> <YYYYMMDD>
    Example: /searchtrains NDLS BCT 20250810
    """
    parts = message.text.strip().split()

    if len(parts) != 4:
        bot.reply_to(
            message,
            "🚂 *Search Trains*\n\n"
            "Usage: `/searchtrains <FROM> <TO> <YYYYMMDD>`\n"
            "Example: `/searchtrains NDLS BCT 20250810`\n\n"
            "Station codes: NDLS, BCT, MAS, CSTM, SBC...",
            parse_mode="Markdown"
        )
        return

    _, from_stn, to_stn, date = parts
    msg = bot.reply_to(message, "🔍 searching trains... hold up bestie 🚂")

    try:
        data = api_search_trains(from_stn, to_stn, date)

        if not data.get("status") or not data.get("data"):
            bot.edit_message_text(
                "😤 no trains found or invalid input. check station codes and date format (YYYYMMDD).",
                msg.chat.id, msg.message_id
            )
            return

        trains = data["data"]
        lines = [f"🚆 *Trains: {from_stn.upper()} → {to_stn.upper()}* ({date})\n"]

        for t in trains[:10]:
            name = t.get("train_name", "N/A")
            number = t.get("train_number", "N/A")
            dep = t.get("from_std", "?")
            arr = t.get("to_std", "?")
            duration = t.get("duration", "?")
            lines.append(f"🔹 *{number}* — {name}")
            lines.append(f"   🕐 {dep} → {arr} ({duration})\n")

        if len(trains) > 10:
            lines.append(f"_...and {len(trains) - 10} more trains_")

        bot.edit_message_text(
            "\n".join(lines),
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.edit_message_text(
            f"❌ api said nah rn\n\n`{e}`",
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )


@bot.message_handler(commands=["availability"])
def availability_cmd(message):
    """Usage: /availability <FROM> <TO> <YYYYMMDD>
    Example: /availability NDLS BCT 20250810
    """
    parts = message.text.strip().split()

    if len(parts) != 4:
        bot.reply_to(
            message,
            "🎫 *Seat Availability*\n\n"
            "Usage: `/availability <FROM> <TO> <YYYYMMDD>`\n"
            "Example: `/availability NDLS BCT 20250810`",
            parse_mode="Markdown"
        )
        return

    _, from_stn, to_stn, date = parts
    msg = bot.reply_to(message, "🔍 checking availability... one sec 🎫")

    try:
        data = api_seat_availability(from_stn, to_stn, date)

        if not data.get("status") or not data.get("data"):
            bot.edit_message_text(
                "😤 no data found. verify station codes and date.",
                msg.chat.id, msg.message_id
            )
            return

        rows = data["data"]
        lines = [f"🎫 *Availability: {from_stn.upper()} → {to_stn.upper()}*\n"]

        for row in rows[:15]:
            date_val = row.get("date", "?")
            status = row.get("current_status", "?")
            cls = row.get("class_type", "?")
            lines.append(f"📅 {date_val} | {cls} | {status}")

        bot.edit_message_text(
            "\n".join(lines),
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.edit_message_text(
            f"❌ api flopped bestie\n\n`{e}`",
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )


@bot.message_handler(commands=["livetrain"])
def livetrain_cmd(message):
    """Usage: /livetrain <TRAIN_NUMBER>
    Example: /livetrain 12301
    """
    parts = message.text.strip().split()

    if len(parts) != 2:
        bot.reply_to(
            message,
            "🟢 *Live Train Status*\n\n"
            "Usage: `/livetrain <TRAIN_NUMBER>`\n"
            "Example: `/livetrain 12301`",
            parse_mode="Markdown"
        )
        return

    train_no = parts[1]
    msg = bot.reply_to(message, f"📡 fetching live status for {train_no}...")

    try:
        data = api_live_train(train_no)

        if not data.get("status") or not data.get("data"):
            bot.edit_message_text(
                "😤 train not found or not running today.",
                msg.chat.id, msg.message_id
            )
            return

        d = data["data"]
        train_name = d.get("trainName", "N/A")
        current_stn = d.get("currentStation", "?")
        delay = d.get("delayInMinutes", 0)
        status = d.get("trainStatus", "?")

        delay_text = f"⚠️ {delay} min late" if delay and int(delay) > 0 else "✅ on time"

        lines = [
            f"🟢 *Live Status: {train_no} — {train_name}*\n",
            f"📍 Current Station: *{current_stn}*",
            f"⏱ Status: {delay_text}",
            f"🚦 Train Status: {status}",
        ]

        upcoming = d.get("upcomingStations", [])
        if upcoming:
            lines.append("\n📋 *Next Stops:*")
            for stn in upcoming[:5]:
                sname = stn.get("stationName", "?")
                sch = stn.get("scheduledArrival", "?")
                exp = stn.get("estimatedArrival", "?")
                lines.append(f"  🔸 {sname} | Sch: {sch} | ETA: {exp}")

        bot.edit_message_text(
            "\n".join(lines),
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.edit_message_text(
            f"❌ live status failed rn\n\n`{e}`",
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )


@bot.message_handler(commands=["pnr"])
def pnr_cmd(message):
    """Usage: /pnr <PNR_NUMBER>
    Example: /pnr 1234567890
    """
    parts = message.text.strip().split()

    if len(parts) != 2:
        bot.reply_to(
            message,
            "🎟️ *PNR Status*\n\n"
            "Usage: `/pnr <PNR_NUMBER>`\n"
            "Example: `/pnr 1234567890`",
            parse_mode="Markdown"
        )
        return

    pnr = parts[1]
    msg = bot.reply_to(message, f"🔍 checking PNR {pnr}...")

    try:
        data = api_pnr_status(pnr)

        if not data.get("status") or not data.get("data"):
            bot.edit_message_text(
                "😤 PNR not found. double check the number bestie.",
                msg.chat.id, msg.message_id
            )
            return

        d = data["data"]
        train_no = d.get("trainNumber", "?")
        train_name = d.get("trainName", "?")
        from_stn = d.get("sourceStation", "?")
        to_stn = d.get("destinationStation", "?")
        doj = d.get("dateOfJourney", "?")
        cls = d.get("classType", "?")
        chart = d.get("chartPrepared", False)

        lines = [
            f"🎟️ *PNR Status: {pnr}*\n",
            f"🚂 {train_no} — {train_name}",
            f"📍 {from_stn} → {to_stn}",
            f"📅 Date: {doj} | Class: {cls}",
            f"📋 Chart: {'✅ Prepared' if chart else '⏳ Not yet'}\n",
            "*Passengers:*"
        ]

        passengers = d.get("passengerList", [])
        for i, p in enumerate(passengers, 1):
            booking = p.get("bookingStatus", "?")
            current = p.get("currentStatus", "?")
            coach = p.get("currentCoachId", "?")
            berth = p.get("currentBerthNo", "?")
            lines.append(
                f"  👤 P{i}: Booked: {booking} | Current: *{current}*"
                + (f" | {coach}-{berth}" if coach != "?" else "")
            )

        bot.edit_message_text(
            "\n".join(lines),
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.edit_message_text(
            f"❌ pnr check failed fr\n\n`{e}`",
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )


@bot.message_handler(commands=["seatavail"])
def seatavail_cmd(message):
    """Usage: /seatavail <trainNo> <src> <dst> <YYYYMMDD> <class> <quota>
    Example: /seatavail 12301 NDLS BCT 20250810 SL GN
    """
    parts = message.text.strip().split()

    if len(parts) != 7:
        bot.reply_to(
            message,
            "💺 *Fetch Seat Availability*\n\n"
            "Usage: `/seatavail <trainNo> <src> <dst> <YYYYMMDD> <class> <quota>`\n"
            "Example: `/seatavail 12301 NDLS BCT 20250810 SL GN`\n\n"
            "Classes: SL, 3A, 2A, 1A, CC, EC\n"
            "Quotas: GN, TQ, LD, PT",
            parse_mode="Markdown"
        )
        return

    _, train_no, src, dst, date, cls, quota = parts
    msg = bot.reply_to(message, f"💺 checking seats on {train_no}...")

    try:
        data = api_fetch_seat_avail(train_no, src, dst, date, cls, quota)

        if not data.get("status") or not data.get("data"):
            bot.edit_message_text(
                "😤 no seat data. check train no, stations, class, quota.",
                msg.chat.id, msg.message_id
            )
            return

        rows = data["data"]
        lines = [
            f"💺 *Seat Availability*\n",
            f"🚂 Train: {train_no} | {src.upper()} → {dst.upper()}",
            f"🎫 Class: {cls.upper()} | Quota: {quota.upper()}\n",
            "*Availability:*"
        ]

        for row in rows[:10]:
            d = row.get("date", "?")
            status = row.get("current_status", "?")
            fare = row.get("total_fare", "")
            fare_text = f" | ₹{fare}" if fare else ""
            lines.append(f"  📅 {d}: *{status}*{fare_text}")

        bot.edit_message_text(
            "\n".join(lines),
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.edit_message_text(
            f"❌ seat check failed bestie\n\n`{e}`",
            msg.chat.id, msg.message_id,
            parse_mode="Markdown"
        )


# --------------------------------------------------
# Catch-all
# --------------------------------------------------

@bot.message_handler(func=lambda m: True)
def unknown(message):
    if not owner_only(message):
        bot.reply_to(
            message,
            "🤨 unknown command bestie\n\ntry /help for available commands 😼"
        )
        return

    bot.reply_to(
        message,
        "🤨 bro what even is this command 💀\n\nbilla said huh.\n\ntry /help bestie"
    )


# --------------------------------------------------
# Start
# --------------------------------------------------

if __name__ == "__main__":
    print("😼 Badmosh Billa Online... no cap")
    threading.Thread(target=run_health_server, daemon=True).start()

    while True:
        try:
            bot.infinity_polling(
                skip_pending=True,
                timeout=30,
                long_polling_timeout=30
            )

        except Exception:
            print(traceback.format_exc())

            import time
            time.sleep(5)
