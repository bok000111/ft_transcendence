from django.urls import path

from ws.consumers import MainConsumer


urlpatterns = [
    path("ws/", MainConsumer.as_asgi(), name="main-ws"),
]
