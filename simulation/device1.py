import paho.mqtt.client as mqtt
import yfinance as yf
import time

# Connect to the same MQTT broker
client = mqtt.Client()
client.on_connect = lambda c, u, f, rc: print(f"Connected to MQTT broker with result code {rc}")
client.connect("localhost", 1883)

stocks = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN']

while True:
    for stock in stocks:
        # fetching live stock price with yfinance
        try:
            stock_data = yf.Ticker(stock)
            price = round(stock_data.history(period="1d").iloc[-1]['Close'], 2)  # Get the latest closing price
            client.publish(f"stocks/{stock}", str(price))  # Publish to topic "stocks/{stock}"
            print(f"Published {stock} price: {price}")
        except Exception as e:
            print(f"Failed to fetch data for {stock}: {e}")
    time.sleep(10)
    print("-----------------------------")
