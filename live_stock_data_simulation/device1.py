import paho.mqtt.client as mqtt
import time
import random

# Connect to the same MQTT broker
client = mqtt.Client()
client.on_connect = lambda c, u, f, rc: print(f"Connected to MQTT broker with result code {rc}")
client.connect("localhost", 1883)

stocks = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN']

while True:
    for stock in stocks:
        price = round(random.uniform(200, 350), 2)  # random price
        client.publish(f"stocks/{stock}", str(price))  # publish to topic "stocks/{stock}"
        print(f"Published {stock} price: {price}")
    # time.sleep(random.randint(1, 5))
    time.sleep(30)
    print("-----------------------------")
