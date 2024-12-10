import logging
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import paho.mqtt.client as mqtt
from dashboard.models import Stock, StockPrice
from iot.models import Device, DeviceSession
from datetime import datetime

logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
        client.subscribe("stocks/#")  # subscribe to all stock topics
        client.subscribe("devices/#")  # Subscribe to device-related topics
    else:
        print(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    try:
        print(f"Received message: {msg.payload.decode('utf-8')} on topic {msg.topic}")

        # Check if the message is device-related
        if msg.topic.startswith("devices/"):
            device_id = msg.topic.split('/')[1]

            # Register the device if not already registered
            device, created = Device.objects.get_or_create(device_id=device_id)
            if created:
                print(f"Registered new device: {device_id}")

            # Check for device connection
            if "connected" in msg.payload.decode('utf-8').lower():
                DeviceSession.objects.create(device=device, ip_address=client._host)
                print(f"Device {device_id} connected.")

            elif "disconnected" in msg.payload.decode('utf-8').lower():
                session = device.sessions.filter(disconnected_at__isnull=True).last()
                if session:
                    session.disconnected_at = datetime.now()
                    session.save()
                    print(f"Device {device_id} disconnected.")

        # Process stock data (existing logic)
        elif msg.topic.startswith("stocks/"):
            topic = msg.topic.split('/')[-1]
            price = float(msg.payload.decode('utf-8'))
            print(f"Processing topic: {topic}, price: {price}")

            # Update stock and broadcast as before
            stock, _ = Stock.objects.get_or_create(ticker=topic)
            stock_price = StockPrice.objects.create(stock=stock, price=price, timestamp=datetime.now())
            print(f"Stock {stock.ticker} updated in DB with price {stock_price.price}")

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
#         print(f"Received message: {msg.payload.decode('utf-8')} on topic {msg.topic}")
#         topic = msg.topic.split('/')[-1]
#         price = float(msg.payload.decode('utf-8'))
#         print(f"Processing topic: {topic}, price: {price}")

#         # update db
#         stock, _ = Stock.objects.get_or_create(ticker=topic)
#         stock_price = StockPrice.objects.create(stock=stock, price=price, timestamp=datetime.now())
#         print(f"Stock {stock.ticker} updated in DB with price {stock_price.price}")

#         # Broadcast WebSocket update
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
#         print(f"Broadcasted update for {stock.ticker}")
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
