import paho.mqtt.client as mqtt
from dashboard.models import Stock, StockPrice
from datetime import datetime
import random

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to all stock topics (e.g., stocks/AAPL, stocks/GOOG)
    client.subscribe("stocks/#")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic.split('/')[-1]  # Extract ticker from topic (e.g., "AAPL" from "stocks/AAPL")
        payload = msg.payload.decode('utf-8')  # Decode payload
        stock, _ = Stock.objects.get_or_create(ticker=topic)  # Get or create the Stock object
        # Simulate price updates
        StockPrice.objects.create(stock=stock, price=float(payload), timestamp=datetime.now())
        print(f"Updated {stock.ticker} with price {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)  # Connect to the MQTT broker (default localhost and port 1883)