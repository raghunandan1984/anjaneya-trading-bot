
# anjaneya_fno_bot.py

import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
import requests
import time
import yfinance as yf

# === CONFIGURATION ===
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your bot token
chat_id = 'YOUR_TELEGRAM_CHAT_ID'      # Replace with your Telegram chat ID

# Replace with F&O enabled stocks from Nifty 50
nifty_fo_stocks = ['RELIANCE.NS', 'INFY.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS']

# Function to send alerts to Telegram
def send_alert(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=payload)
    print("Alert sent:", message if response.status_code == 200 else response.text)

# Function to fetch and prepare price data
def get_price_data(symbol):
    df = yf.download(symbol, period="3mo", interval="1d")
    df = df['Close'].to_frame(name='close')  # Ensure it's a Series and rename to 'close'
    return df

# === Main Scanning Logic ===
for symbol in nifty_fo_stocks:
    df = get_price_data(symbol)
    if df is None or df.empty or len(df) < 60:
        print(f"Skipping {symbol}: Not enough data")
        continue

    df['ema20'] = EMAIndicator(df['close'], window=20).ema_indicator()
    df['ema50'] = EMAIndicator(df['close'], window=50).ema_indicator()
    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()

    latest = df.iloc[-1]
    if latest['ema20'] > latest['ema50'] and latest['rsi'] > 50:
        send_alert(f"{symbol}: BUY Signal - EMA20 above EMA50, RSI: {round(latest['rsi'],2)}")
    elif latest['ema20'] < latest['ema50'] and latest['rsi'] < 50:
        send_alert(f"{symbol}: SELL Signal - EMA20 below EMA50, RSI: {round(latest['rsi'],2)}")
    else:
        print(f"{symbol}: No clear signal.")

    time.sleep(1)  # Avoid hitting API rate limits
