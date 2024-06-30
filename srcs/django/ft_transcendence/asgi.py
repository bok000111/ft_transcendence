# fmt: off
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import CookieMiddleware
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

# 사용자 정의 모듈은 django_asgi_app 초기화 이후에 import 해야 함
from ws.middleware import JWTChannelAuthMiddleware
from ws.routing import urlpatterns
# fmt: on

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            CookieMiddleware(JWTChannelAuthMiddleware(URLRouter(urlpatterns)))
        ),
    }
)
