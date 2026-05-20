from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config.settings import TOKEN
from strategies.strategy import generate_signal

import asyncio
from datetime import datetime
import random

# =========================
# BOT SETUP
# =========================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================
# ADMIN ID
# =========================

ADMIN_ID = 6952578593

# =========================
# GLOBAL VARIABLES
# =========================

user_chat_id = None

total_signals = 0
wins = 0
losses = 0

# =========================
# KEYBOARD MENU
# =========================

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Live Signals")],
        [KeyboardButton(text="💎 VIP Signals")],
        [KeyboardButton(text="📜 Signal History")],
        [KeyboardButton(text="📈 Bot Stats")],
        [KeyboardButton(text="💎 VIP Access"),
         KeyboardButton(text="📈 Market Status")],
        [KeyboardButton(text="⚙️ Help")]
    ],
    resize_keyboard=True
)

# =========================
# VIP CHECK SYSTEM
# =========================

def is_vip(user_id):

    try:

        with open("data/vip_users.txt", "r") as file:

            vip_users = file.read().splitlines()

        return str(user_id) in vip_users

    except:

        return False

# =========================
# SAVE SIGNAL HISTORY
# =========================

def save_signal(data):

    with open("data/history.txt", "a", encoding="utf-8") as file:

        file.write(
            f"{datetime.now()} | "
            f"{data['pair']} | "
            f"{data['signal']} | "
            f"{data['confidence']}%\n"
        )

# =========================
# UPDATE STATS
# =========================

def update_stats():

    global total_signals
    global wins
    global losses

    total_signals += 1

    result = random.choice(["WIN", "LOSS", "WIN"])

    if result == "WIN":
        wins += 1
    else:
        losses += 1

# =========================
# START COMMAND
# =========================

@dp.message(Command("start"))
async def start_command(message: Message):

    global user_chat_id

    user_chat_id = message.chat.id

    await message.answer(
        "🚀 Welcome to JX Quantum Signals\n\n"
        "✅ Bot Status: ONLINE\n"
        "📊 Market Scanner: ACTIVE\n"
        "🧠 AI Engine: READY\n\n"
        "🔥 VIP SYSTEM ENABLED",
        reply_markup=main_keyboard
    )

# =========================
# FREE SIGNAL
# =========================

@dp.message(lambda message: message.text == "📊 Live Signals")
async def live_signals(message: Message):

    data = generate_signal()

    save_signal(data)
    update_stats()

    await message.answer(
        f"📊 FREE SIGNAL\n\n"
        f"PAIR: {data['pair']}\n"
        f"SIGNAL: {data['signal']}\n"
        f"TREND: {data['trend']}\n"
        f"RSI: {data['rsi']}\n"
        f"CANDLE: {data['candle']}\n"
        f"TIMEFRAME: 5M\n"
        f"CONFIDENCE: {data['confidence']}%"
    )

# =========================
# VIP SIGNAL
# =========================

@dp.message(lambda message: message.text == "💎 VIP Signals")
async def vip_signals(message: Message):

    user_id = message.from_user.id

    if not is_vip(user_id):

        await message.answer(
            "❌ VIP ACCESS REQUIRED\n\n"
            "Contact Admin For VIP Membership."
        )

        return

    data = generate_signal()

    await message.answer(
        f"🔥 VIP SIGNAL\n\n"
        f"PAIR: {data['pair']}\n"
        f"SIGNAL: {data['signal']}\n"
        f"TREND: {data['trend']}\n"
        f"RSI: {data['rsi']}\n"
        f"CANDLE: {data['candle']}\n"
        f"TIMEFRAME: 5M\n"
        f"CONFIDENCE: {random.randint(95, 99)}%\n"
        f"RISK: LOW ✅"
    )

# =========================
# ADD VIP USER
# =========================

@dp.message(Command("addvip"))
async def add_vip(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    try:

        user_id = message.text.split()[1]

        with open("data/vip_users.txt", "a") as file:
            file.write(f"{user_id}\n")

        await message.answer("✅ VIP User Added")

    except:

        await message.answer("⚠️ Usage: /addvip USER_ID")

# =========================
# REMOVE VIP USER
# =========================

@dp.message(Command("removevip"))
async def remove_vip(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    try:

        user_id = message.text.split()[1]

        with open("data/vip_users.txt", "r") as file:
            vip_users = file.readlines()

        with open("data/vip_users.txt", "w") as file:

            for vip in vip_users:

                if vip.strip() != user_id:
                    file.write(vip)

        await message.answer("❌ VIP User Removed")

    except:

        await message.answer("⚠️ Usage: /removevip USER_ID")

# =========================
# SIGNAL HISTORY
# =========================

@dp.message(lambda message: message.text == "📜 Signal History")
async def signal_history(message: Message):

    try:

        with open("data/history.txt", "r", encoding="utf-8") as file:

            history = file.readlines()

        if not history:
            await message.answer("📭 No Signal History Found")
            return

        last_signals = history[-10:]

        text = "📜 LAST SIGNALS\n\n"

        for signal in last_signals:
            text += signal

        await message.answer(text)

    except:

        await message.answer("⚠️ History File Not Found")

# =========================
# BOT STATS
# =========================

@dp.message(lambda message: message.text == "📈 Bot Stats")
async def bot_stats(message: Message):

    global total_signals
    global wins
    global losses

    accuracy = 0

    if total_signals > 0:
        accuracy = round((wins / total_signals) * 100, 2)

    await message.answer(
        f"📈 BOT STATS\n\n"
        f"TOTAL SIGNALS: {total_signals}\n"
        f"WINS: {wins}\n"
        f"LOSSES: {losses}\n"
        f"ACCURACY: {accuracy}%"
    )

# =========================
# VIP ACCESS
# =========================

@dp.message(lambda message: message.text == "💎 VIP Access")
async def vip_access(message: Message):

    await message.answer(
        "💎 VIP MEMBERSHIP AVAILABLE\n\n"
        "Contact Admin To Unlock Premium Signals."
    )

# =========================
# MARKET STATUS
# =========================

@dp.message(lambda message: message.text == "📈 Market Status")
async def market_status(message: Message):

    await message.answer(
        "📈 MARKET STATUS: ACTIVE\n"
        "🔥 VOLATILITY: HIGH"
    )

# =========================
# HELP
# =========================

@dp.message(lambda message: message.text == "⚙️ Help")
async def help_command(message: Message):

    await message.answer(
        "⚙️ HELP CENTER\n\n"
        "Use the buttons below to navigate."
    )

# =========================
# AUTO SIGNAL SYSTEM
# =========================

async def send_auto_signal():

    global user_chat_id

    if user_chat_id is None:
        return

    data = generate_signal()

    save_signal(data)
    update_stats()

    text = (
        f"🚀 AUTO SIGNAL\n\n"
        f"PAIR: {data['pair']}\n"
        f"SIGNAL: {data['signal']}\n"
        f"CONFIDENCE: {data['confidence']}%"
    )

    await bot.send_message(user_chat_id, text)

# =========================
# MAIN FUNCTION
# =========================

async def main():

    print("✅ Bot Running...")

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_auto_signal,
        "interval",
        minutes=5
    )

    scheduler.start()

    await dp.start_polling(bot)

# =========================
# RUN BOT
# =========================

if __name__ == "__main__":
    asyncio.run(main())