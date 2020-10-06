from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from reel.routing import router as reel_router


application = ProtocolTypeRouter(
    {
        # (http->django views are added by default)
        "websocket": AuthMiddlewareStack(reel_router),
    }
)
