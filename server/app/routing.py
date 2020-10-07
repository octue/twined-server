# from channels.auth import AuthMiddlewareStack
import reel.routing
from channels.routing import ProtocolTypeRouter, URLRouter


application = ProtocolTypeRouter(
    {
        # (http->django views are added by default)
        "websocket": URLRouter(reel.routing.websocket_urlpatterns),
    }
)
