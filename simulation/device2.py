import paho.mqtt.client as mqtt
import yfinance as yf
import time


DEVICE_ID = "D-2"

# Connect to the same MQTT broker
client = mqtt.Client(client_id=DEVICE_ID, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = lambda c, u, f, rc: print(f"Connected to MQTT broker with result code {rc}")
client.connect("localhost", 1883)

stocks = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN']

def publish_device_status(status):
    """
    Publish a message to the device's topic to report its status.
    """
    client.publish(f"devices/{DEVICE_ID}", status)
    print(f"Published device status: {status}")

# Notify the broker that the device has connected
publish_device_status("connected")

try:
    while True:
        for stock in stocks:
            # Fetching live stock price with yfinance
            try:
                stock_data = yf.Ticker(stock)
                price = round(stock_data.history(period="1d").iloc[-1]['Close'], 2)  # Get the latest closing price
                client.publish(f"stocks/{stock}", str(price))  # Publish to topic "stocks/{stock}"
                print(f"Published {stock} price: {price}")
            except Exception as e:
                print(f"Failed to fetch data for {stock}: {e}")
        time.sleep(10)
        print("-----------------------------")
except KeyboardInterrupt:
    # Notify the broker that the device is disconnecting
    publish_device_status("disconnected")
    print("Device disconnected gracefully.")
