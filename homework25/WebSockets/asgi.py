import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import push_notifications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebSockets.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            push_notifications.routing.websocket_urlpatterns
        )
    ),
})
