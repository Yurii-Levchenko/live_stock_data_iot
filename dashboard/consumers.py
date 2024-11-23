import json
from channels.generic.websocket import AsyncWebsocketConsumer
from dashboard.models import StockPrice

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Join a stock ticker group (you can customize this)
        await self.channel_layer.group_add("stock_updates", self.channel_name)

    async def disconnect(self, close_code):
        # Leave the stock ticker group
        await self.channel_layer.group_discard("stock_updates", self.channel_name)

    async def send_stock_update(self, event):
        # Send stock data to WebSocket
        await self.send(text_data=json.dumps(event['data']))
