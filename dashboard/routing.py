from django.urls import path
from .consumers import StockConsumer

websocket_urlpatterns = [
    path('ws/stocks/', StockConsumer.as_asgi()),
]
