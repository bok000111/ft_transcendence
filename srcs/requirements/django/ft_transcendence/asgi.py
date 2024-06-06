import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ft_transcendence.settings")

django_asgi_app = get_asgi_application()

from ws.middlewares import AuthReqMiddlewareStack
from ws.routing import urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthReqMiddlewareStack(URLRouter(urlpatterns)),
    }
)
