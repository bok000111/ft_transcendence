# fmt: off
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

django_asgi_app = get_asgi_application()

# asgi 초기화 이후에 import 해야함
from ws.routing import urlpatterns
# fmt: on

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(urlpatterns)),
    }
)
