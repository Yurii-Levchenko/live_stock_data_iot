import logging
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import paho.mqtt.client as mqtt
from dashboard.models import Stock, StockPrice
from iot.models import Device, DeviceSession
from datetime import datetime
from decimal import Decimal
from django.utils.timezone import now
from django.core.cache import cache
import json

logger = logging.getLogger(__name__)

# Cache for last known prices to compare for significant change
price_cache = {}
PRICE_CHANGE_THRESHOLD = 0.01  # 1%

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
        client.subscribe("stocks/#")
        client.subscribe("devices/#")
        print("Subscribed to topics: stocks/#, devices/#")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')
        payload = msg.payload.decode('utf-8')
        print(f"[MQTT] Received '{payload}' on topic '{msg.topic}'")

        # ========== DEVICE HANDLING ==========
        if topic_parts[0] == "devices":
            device_id = topic_parts[1]
            device, created = Device.objects.get_or_create(device_id=device_id)
            if created:
                print(f"Registered new device: {device_id}")

            if "connected" in payload.lower():
                DeviceSession.objects.create(device=device, ip_address=client._host)
                print(f"Device {device_id} connected.")

            elif "disconnected" in payload.lower():
                session = device.sessions.filter(disconnected_at__isnull=True).last()
                if session:
                    session.disconnected_at = datetime.now()
                    session.save()
                    print(f"Device {device_id} disconnected.")

        # ========== STOCK DATA HANDLING ==========
        elif topic_parts[0] == "stocks" and len(topic_parts) == 3:
            ticker = topic_parts[1].upper()
            subtopic = topic_parts[2]

            # === WebSocket Broadcast ===
            stock, _ = Stock.objects.get_or_create(ticker=ticker)

            if subtopic == "price":
                    new_price = Decimal(payload)
                    last_price = price_cache.get(ticker)
                    price_cache[ticker] = new_price  # Always update cache

                    # === WebSocket Broadcast ===
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "stock_updates",
                        {
                            "type": "send_stock_update",
                            "data": {
                                "ticker": stock.ticker,
                                "price": float(new_price),
                                "timestamp": now().strftime('%Y-%m-%d %H:%M:%S'),
                                "market_status": getattr(stock, "market_status", "N/A"),
                                "exchange": getattr(stock, "exchange", "N/A"),
                            },
                        },
                    )
                    print(f"[WS] Broadcasted update for {stock.ticker} at {new_price}")


                    # === Redis Cache Update ===
                    cache.set(f"stock_price_{ticker}", new_price, timeout=300)  # Cache for 5 minutes
                    cache_stock_price(ticker, new_price, now().strftime('%Y-%m-%d %H:%M:%S'))
                    

                    # === DB Save Only If Significant ===
                    if (
                        last_price is None or
                        abs((new_price - last_price) / last_price) >= Decimal(PRICE_CHANGE_THRESHOLD)
                    ):
                        stock_price = StockPrice.objects.create(stock=stock, price=new_price, recorded_at=now())
                        print(f"[DB] Stored price for {stock.ticker}: {new_price}")
                        

            elif subtopic == "timestamp":
                # Could be used to update UI cache or add extra model logic
                print(f"{ticker} timestamp: {payload}")

            elif subtopic == "market_status":
                print(f"{ticker} market status: {payload}")
                stock.market_status = payload
                stock.save(update_fields=["market_status"])

            elif subtopic == "exchange":
                print(f"{ticker} exchange: {payload}")
                if not stock.exchange:
                    stock.exchange = payload
                    stock.save(update_fields=["exchange"])

    except Exception as e:
        logger.error(f"Error processing message on topic {msg.topic}: {e}")

def cache_stock_price(ticker, price, timestamp):
    key = f"stock:prices:{ticker}"
    value = json.dumps({"price": float(price), "timestamp": timestamp})
    cache.get_client().lpush(key, value)
    cache.get_client().ltrim(key, 0, 9999)  # Keep last 10,000 updates

# MQTT configuration
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

client.connect(
    settings.MQTT_SERVER, 
    settings.MQTT_PORT, 
    # settings.MQTT_KEEPALIVE
)
client.loop_start()  # <- Very important!
# client.loop_forever()