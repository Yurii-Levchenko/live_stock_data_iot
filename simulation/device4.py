import paho.mqtt.client as mqtt
import yfinance as yf
import time
from datetime import datetime
import pytz
from creds import FINNHUB_API_KEY
import finnhub

# ========== CONFIGURATION ==========
DEVICE_ID = "D-4"
BROKER_HOST = "localhost"
BROKER_PORT = 1883
STOCKS = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN']
PUBLISH_INTERVAL = 10  # seconds

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
# ===================================

# MQTT client setup
client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = lambda c, u, f, rc: print(f"Connected to MQTT broker with result code {rc}")
client.connect(BROKER_HOST, BROKER_PORT)

# Publish device status
def publish_device_status(status):
    topic = f"devices/{DEVICE_ID}"
    client.publish(topic, status)
    print(f"[STATUS] {status} -> {topic}")

# Fetch exchange and timezone info using SDK
def fetch_stock_info(symbol):
    profile = finnhub_client.company_profile2(symbol=symbol)
    return {
        "exchange": profile.get("exchange"),
        "timezone": profile.get("timezone"),
    }

# Fetch market status using SDK
def fetch_market_status(exchange_code):
    try:
        data = finnhub_client.market_status(exchange=exchange_code)
        return {
            "exchange": data.get("exchange"),
            "is_open": data.get("isOpen"),
            "session": data.get("session"),
            "timezone": data.get("timezone"),
        }
    except Exception as e:
        print(f"[ERROR] Could not fetch market status for {exchange_code}: {e}")
        return {
            "exchange": exchange_code,
            "is_open": None,
            "session": None,
            "timezone": None,
        }

# Fetch live stock price using yfinance
def fetch_live_price(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d", interval="1m")
    if history.empty:
        raise ValueError(f"No intraday data for {ticker}")
    latest = history.iloc[-1]
    return round(latest['Close'], 2), latest.name.to_pydatetime()

# Startup
publish_device_status("connected")

try:
    while True:
        for stock in STOCKS:
            try:
                price, ts = fetch_live_price(stock)
                info = fetch_stock_info(stock)
                market_info = fetch_market_status(info['exchange'])

                # Convert to user's local timezone if available
                timestamp_local = ts.astimezone(pytz.timezone(info['timezone'])) if info['timezone'] else ts

                message = {
                    "price": price,
                    "timestamp": timestamp_local.isoformat(),
                    "market": market_info['exchange'],
                    "market_status": "open" if market_info['is_open'] else "closed",
                    "session": market_info['session'],
                    "exchange": info['exchange'],
                }

                topic = f"stocks/{stock}"
                client.publish(topic, str(message))
                print(f"[DATA] {stock} -> {message}")
            except Exception as e:
                print(f"[ERROR] {stock}: {e}")
        time.sleep(PUBLISH_INTERVAL)
        print("-" * 40)
except KeyboardInterrupt:
    publish_device_status("disconnected")
    print("Device disconnected gracefully.")
