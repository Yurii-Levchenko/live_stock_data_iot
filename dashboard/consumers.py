import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connection attempt...")
        await self.accept()
        # join a stock ticker group
        await self.channel_layer.group_add("stock_updates", self.channel_name)
        print(f"WebSocket connection established: {self.channel_name}")

    async def disconnect(self, close_code):
        # leave the stock ticker group
        await self.channel_layer.group_discard("stock_updates", self.channel_name)
        print(f"WebSocket connection closed: {self.channel_name}")

    async def send_stock_update(self, event):
        # send stock data to WebSocket
        print(f"Sending stock update: {event['data']}")
        await self.send(text_data=json.dumps(event['data']))
        print(f"Sent stock update to WebSocket: {event['data']}")
