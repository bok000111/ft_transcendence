from ws.consumers import MainConsumer

from django.urls import path


urlpatterns = [
    path("ws/", MainConsumer.as_asgi(), name="main-ws"),
]
