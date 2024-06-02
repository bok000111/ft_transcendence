from django.urls import path
from channels.routing import URLRouter

# from lobby.routing import urlpatterns as lobby_urlpatterns
# from ..ft_transcendence import routing
from . import consumers


urlpatterns = [
    path("ws/", consumers.WSConsumer.as_asgi(), name="ws"),
]
