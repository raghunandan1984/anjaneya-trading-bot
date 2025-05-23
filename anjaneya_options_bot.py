
# anjaneya_options_bot.py

import requests
import datetime

# === CONFIGURATION ===
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
chat_id = 'YOUR_TELEGRAM_CHAT_ID'

# === Mock Data ===
nifty_spot_price = 22350  # Replace with live data later
rsi_value = 65            # Simulated RSI
ema_fast = 22310
ema_slow = 22280

# === Options Strategy Logic ===
def decide_option_trade(spot, rsi, ema_fast, ema_slow):
    if ema_fast > ema_slow and rsi > 60:
        strike = round(spot / 50) * 50 + 50
        return f"BUY NIFTY {strike} CE (Bullish crossover with RSI {rsi})"
    elif ema_fast < ema_slow and rsi < 40:
        strike = round(spot / 50) * 50 - 50
        return f"BUY NIFTY {strike} PE (Bearish crossover with RSI {rsi})"
    else:
        return "No trade signal - market unclear"

# === Telegram Alert ===
def send_alert(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=payload)
    print("Alert sent:", message if response.status_code == 200 else response.text)

# === Main Bot Execution ===
decision = decide_option_trade(nifty_spot_price, rsi_value, ema_fast, ema_slow)
send_alert(f"Anjaneya Option Bot Signal: {decision}")
