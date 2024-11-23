"""
ASGI config for live_stock_data_iot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from iot.mqtt import client as mqtt_client  # Import of MQTT client
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from dashboard.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "live_stock_data_iot.settings")

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})


mqtt_client.loop_start()  # Start the MQTT loop