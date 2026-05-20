import random
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

pairs = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "AUD/USD",
    "USD/CAD"
]

def analyze_pair(pair):

    # Smart Simulated Market Data
    prices = np.cumsum(np.random.normal(0, 1, 100)) + 100

    df = pd.DataFrame(prices, columns=["close"])

    # EMA
    ema9 = EMAIndicator(df["close"], window=9).ema_indicator()
    ema21 = EMAIndicator(df["close"], window=21).ema_indicator()

    # RSI
    rsi = RSIIndicator(df["close"], window=14).rsi()

    latest_rsi = float(rsi.iloc[-1])
    latest_ema9 = float(ema9.iloc[-1])
    latest_ema21 = float(ema21.iloc[-1])

    # Candle Strength
    candle_strength = random.randint(1, 100)

    # Default
    signal = "WAIT ⚪"
    trend = "SIDEWAYS"
    candle = "WEAK"
    confidence = random.randint(70, 80)

    # Strong CALL
    if (
        latest_ema9 > latest_ema21
        and latest_rsi > 60
        and candle_strength > 70
    ):

        signal = "CALL 🟢"
        trend = "BULLISH"
        candle = "STRONG BULLISH"
        confidence = random.randint(90, 98)

    # Strong PUT
    elif (
        latest_ema9 < latest_ema21
        and latest_rsi < 40
        and candle_strength > 70
    ):

        signal = "PUT 🔴"
        trend = "BEARISH"
        candle = "STRONG BEARISH"
        confidence = random.randint(90, 98)

    return {
        "pair": pair,
        "signal": signal,
        "trend": trend,
        "rsi": round(latest_rsi, 2),
        "candle": candle,
        "confidence": confidence
    }

def generate_signal():

    best_signal = None

    for pair in pairs:

        data = analyze_pair(pair)

        if best_signal is None:
            best_signal = data

        elif data["confidence"] > best_signal["confidence"]:
            best_signal = data

    return best_signal