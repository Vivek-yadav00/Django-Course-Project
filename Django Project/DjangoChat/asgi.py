"""
ASGI config for DjangoChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""
# ASynchronous Server Gateway Interface (ASGI) configuration
# This file is used to deploy the Django application using ASGI-compatible web servers.
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoChat.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import chatix.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatix.routing.websocket_urlpatterns
        )
    )
})
