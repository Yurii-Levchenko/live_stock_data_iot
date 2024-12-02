import logging
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import paho.mqtt.client as mqtt
from dashboard.models import Stock, StockPrice
from datetime import datetime

logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
        client.subscribe("stocks/#")  # subscribe to all stock topics
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        print(f"Received message: {msg.payload.decode('utf-8')} on topic {msg.topic}")
        topic = msg.topic.split('/')[-1]
        price = float(msg.payload.decode('utf-8'))
        print(f"Processing topic: {topic}, price: {price}")

        # update db
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


# MQTT configuration
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(
    settings.MQTT_SERVER, 
    settings.MQTT_PORT, 
    # settings.MQTT_KEEPALIVE
)
