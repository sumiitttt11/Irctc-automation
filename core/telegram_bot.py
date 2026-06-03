import json
import os
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
# Commands
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
        "📖 /help  — full command list\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🤖 ready to cook boss. no cap.\n\n"
        "🔫 phew phew"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["help"])
def help_cmd(message):
    if not owner_only(message):
        return unauthorized(message)

    bot.reply_to(
        message,
        "😼🔫 BADMOSH BILLA — COMMAND DROP\n\n"
        "━━━━━━━━━━━━━━━\n"
        "📊 VIBE CHECKS\n"
        "━━━━━━━━━━━━━━━\n"
        "👀 /status  — full status lowdown\n"
        "⚙️ /settings  — current config\n"
        "🟢 /health  — health check\n"
        "💓 /ping  — billa alive?\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🚂 BOOKING INTEL\n"
        "━━━━━━━━━━━━━━━\n"
        "🚆 /trains  — train list\n"
        "👥 /passengers  — squad list\n"
        "📅 /date  — journey date\n"
        "🎫 /quota  — quota type\n"
        "⏰ /firetime  — when to fire\n"
        "💳 /payment  — payment method\n\n"
        "━━━━━━━━━━━━━━━\n"
        "😼 BILLA ZONE\n"
        "━━━━━━━━━━━━━━━\n"
        "😺 /about  — origin story\n"
        "📜 /logs  — last logs\n"
        "🔄 /restart  — reincarnation\n"
        "🥛 /donate  — fuel the cat\n\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🤖 status: online\n"
        "🔒 access: owner only (except /donate, that's public bestie)\n"
        "🚂 mode: tatkal ready\n\n"
        "🔫 phew phew boss!"
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
# Catch-all
# --------------------------------------------------

@bot.message_handler(func=lambda m: True)
def unknown(message):
    if not owner_only(message):
        return unauthorized(message)

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
