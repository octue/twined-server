import reel.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


application = ProtocolTypeRouter(
    {
        # (http->django views are added by default)
        "websocket": AuthMiddlewareStack(URLRouter(reel.routing.websocket_urlpatterns)),
    }
)
