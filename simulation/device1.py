import paho.mqtt.client as mqtt
import yfinance as yf
import time

# ========== CONFIGURATION ==========
DEVICE_ID = "D-1"
BROKER_HOST = "localhost"
BROKER_PORT = 1883
STOCKS = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN']
PUBLISH_INTERVAL = 10  # seconds
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

# Fetch live stock price using yfinance
def fetch_live_price(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d", interval="1m")
    if history.empty:
        raise ValueError(f"No intraday data for {ticker}")
    return round(history.iloc[-1]['Close'], 2)

# Startup
publish_device_status("connected")

try:
    while True:
        for stock in STOCKS:
            try:
                price = fetch_live_price(stock)
                topic = f"stocks/{stock}"
                client.publish(topic, str(price))
                print(f"[DATA] {stock}: ${price} -> {topic}")
            except Exception as e:
                print(f"[ERROR] Failed to fetch data for {stock}: {e}")
        time.sleep(PUBLISH_INTERVAL)
        print("-" * 40)
except KeyboardInterrupt:
    publish_device_status("disconnected")
    print("Device disconnected gracefully.")
