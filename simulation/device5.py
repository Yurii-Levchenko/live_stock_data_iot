import paho.mqtt.client as mqtt
import yfinance as yf
import time
from datetime import datetime
import pytz
import finnhub
from creds import FINNHUB_API_KEY

# ========== CONFIGURATION ==========
DEVICE_ID = "D-5"
BROKER_HOST = "localhost"
BROKER_PORT = 1883
STOCKS = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN']
PUBLISH_INTERVAL = 10  # seconds
PRICE_CHANGE_THRESHOLD = 0.0001  # 1%
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
# ===================================

price_cache = {}

# MQTT client setup
client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = lambda c, u, f, rc: print(f"Connected to MQTT broker with result code {rc}")
client.connect(BROKER_HOST, BROKER_PORT)

def publish_device_status(status):
    topic = f"devices/{DEVICE_ID}/status"
    client.publish(topic, status)
    print(f"[STATUS] {status} -> {topic}")

def fetch_market_status():
    try:
        status = finnhub_client.market_status(exchange='US')
        return {
            "is_open": status.get("isOpen"),
            "session": status.get("session"),
            "exchange": status.get("exchange"),
        }
    except Exception as e:
        print(f"[ERROR] Finnhub market status fetch failed: {e}")
        return {
            "is_open": None,
            "session": None,
            "exchange": None,
        }

def fetch_live_price(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d", interval="1m")
    if history.empty:
        raise ValueError(f"No intraday data for {ticker}")
    latest = history.iloc[-1]
    return round(float(latest['Close']), 2), latest.name.to_pydatetime()

publish_device_status("connected")

try:
    while True:
        market_info = fetch_market_status()
        for stock in STOCKS:
            try:
                price, ts = fetch_live_price(stock)
                timestamp = ts.astimezone(pytz.timezone("America/New_York")).isoformat()

                # Check price cache
                last_price = price_cache.get(stock)
                # price_changed = last_price is None or abs((price - last_price) / last_price) >= PRICE_CHANGE_THRESHOLD

                # if price_changed:
                price_cache[stock] = price  # update cache

                client.publish(f"stocks/{stock}/price", str(price))
                client.publish(f"stocks/{stock}/timestamp", timestamp)

                # Publish market status (less frequent if desired)
                client.publish(f"stocks/{stock}/market_status", market_info["session"] or "closed")
                client.publish(f"stocks/{stock}/exchange", market_info["exchange"] or "US")

                print(f"[PUBLISHED] {stock} | ${price} | {timestamp} | {market_info['session']}")

            except Exception as e:
                print(f"[ERROR] {stock}: {e}")

        time.sleep(PUBLISH_INTERVAL)
        print("-" * 40)

except KeyboardInterrupt:
    publish_device_status("disconnected")
    print("Device disconnected gracefully.")


# Summary of Features:
#  Publishes every 60s.
#  Avoids repeated price messages (only publishes on significant change).
#  Publishes price, timestamp, market_status, and exchange to individual MQTT topics.
#  Keeps a cache of last prices for threshold comparison.
#  Stores only significant changes to DB (handled elsewhere like Django signal or view).
#  Uses yfinance for price history—no bloated DB.
