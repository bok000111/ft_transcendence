from django.urls import path
from channels.routing import URLRouter

from pong.routing import urlpatterns as pong_urlpatterns

urlpatterns = [
    # path("ws/pong/", URLRouter(pong_urlpatterns)),
]
