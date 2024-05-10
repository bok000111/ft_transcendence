from django.urls import path
from channels.routing import URLRouter

from lobby.routing import urlpatterns as lobby_urlpatterns

urlpatterns = [
    path("ws/lobby/", URLRouter(lobby_urlpatterns)),
]
