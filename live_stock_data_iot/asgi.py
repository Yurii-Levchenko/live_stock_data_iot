"""
ASGI config for live_stock_data_iot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import logging
from django.core.asgi import get_asgi_application
from iot.mqtt import client as mqtt_client  # Import of MQTT client
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from dashboard.routing import websocket_urlpatterns


logger = logging.getLogger(__name__)

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


try:
    mqtt_client.loop_start()  # Start the MQTT loop
    print("MQTT client started")
except Exception as e:
    logger.error(f"Failed to start MQTT client: {e}")