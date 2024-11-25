import logging
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from dashboard.models import Stock, StockPrice
from datetime import datetime
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
        client.subscribe("stocks/#")  # Subscribe to all stock topics
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    from dashboard.models import Stock, StockPrice
    from datetime import datetime

    try:
        print(f"Received message: {msg.payload.decode('utf-8')} on topic {msg.topic}")
        topic = msg.topic.split('/')[-1]
        price = float(msg.payload.decode('utf-8'))
        print(f"Processing topic: {topic}, price: {price}")

        # Update database
        stock, _ = Stock.objects.get_or_create(ticker=topic)
        stock_price = StockPrice.objects.create(stock=stock, price=price, timestamp=datetime.now())
        print(f"Stock {stock.ticker} updated in DB with price {stock_price.price}")

        # Broadcast WebSocket update
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "stock_updates",
            {
                "type": "send_stock_update",
                "data": {
                    "ticker": stock.ticker,
                    "price": stock_price.price,
                    "timestamp": stock_price.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                },
            },
        )
        print(f"Broadcasted update for {stock.ticker}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

# def on_message(client, userdata, msg):
#     try:
#         print(f"Received message: {msg.payload} on topic {msg.topic}")
#         topic = msg.topic.split('/')[-1]
#         price = float(msg.payload.decode('utf-8'))
        
#         # Update database
#         stock, _ = Stock.objects.get_or_create(ticker=topic)
#         stock_price = StockPrice.objects.create(stock=stock, price=price, timestamp=datetime.now())

#         # Broadcast the update to WebSocket group
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "stock_updates",
#             {
#                 "type": "send_stock_update",
#                 "data": {
#                     "ticker": stock.ticker,
#                     "price": float(stock_price.price),
#                     "timestamp": stock_price.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#                 },
#             },
#         )
#         print(f"Broadcast update for {stock.ticker}: ${price}")
#     except Exception as e:
#         logger.error(f"Error processing message: {e}")

# MQTT configuration
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(
    settings.MQTT_SERVER, 
    settings.MQTT_PORT, 
    # settings.MQTT_KEEPALIVE
)





# import paho.mqtt.client as mqtt
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# # from dashboard.models import Stock, StockPrice
# # from datetime import datetime
# import random

# def on_connect(client, userdata, flags, rc):
#     print("Connected to MQTT broker with result code " + str(rc))
#     # Subscribe to all stock topics (e.g., stocks/AAPL, stocks/GOOG)
#     client.subscribe("stocks/#")


# def on_message(client, userdata, msg):
#     from dashboard.models import Stock, StockPrice
#     from datetime import datetime

#     try:
#         print(f"Received message: {msg.payload} on topic {msg.topic}")
#         topic = msg.topic.split('/')[-1]
#         price = float(msg.payload.decode('utf-8'))
#         stock, _ = Stock.objects.get_or_create(ticker=topic)
#         stock_price = StockPrice.objects.create(stock=stock, price=price, timestamp=datetime.now())
        
#         # Broadcast the update to WebSocket group
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "stock_updates",
#             {
#                 "type": "send_stock_update",
#                 "data": {
#                     "ticker": stock.ticker,
#                     "price": stock_price.price,
#                     "timestamp": stock_price.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#                 },
#             },
#         )
#         print(f"Broadcast update for {stock.ticker}: ${price}")
#     except Exception as e:
#         print(f"Error processing message: {e}")


# def on_message(client, userdata, msg):
#     from dashboard.models import Stock, StockPrice
#     from datetime import datetime
#     import json

#     try:
#         topic = msg.topic.split('/')[-1]  # Extract the stock ticker from the topic
#         price = float(msg.payload.decode('utf-8'))  # Decode and parse the stock price
#         stock, created = Stock.objects.get_or_create(ticker=topic)  # Get or create the Stock
#         StockPrice.objects.create(stock=stock, price=price, timestamp=datetime.now())  # Save price
#         print(f"Updated {stock.ticker} with price {price}")
#     except Exception as e:
#         print(f"Error processing message: {e}")

# def on_message(client, userdata, msg):
#     try:
#         topic = msg.topic.split('/')[-1]  # Extract ticker from topic (e.g., "AAPL" from "stocks/AAPL")
#         payload = msg.payload.decode('utf-8')  # Decode payload
#         stock, _ = Stock.objects.get_or_create(ticker=topic)  # Get or create the Stock object
#         # Simulate price updates
#         StockPrice.objects.create(stock=stock, price=float(payload), timestamp=datetime.now())
#         print(f"Updated {stock.ticker} with price {payload}")
#     except Exception as e:
#         print(f"Error processing message: {e}")

# Initialize MQTT client
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect("localhost", 1883)  # Connect to the MQTT broker (default localhost and port 1883)