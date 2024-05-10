from django.urls import re_path

from . import consumers

urlpatterns = [
    re_path(
        r"(?P<lobby_id>\d+)/$",
        consumers.AGameRoomConsumer.as_asgi(),
        name="ws_game_room",
    ),
]
