# pong/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("create/", views.create_view, name="create_game_room"),
    path("<int:room_id>/", views.by_id_view, name="get_room_by_id"),
    # path("join/", views.join_view, name="join"),
    # path("leave/", views.leave_view, name="leave"), # Not implemented
    # path("ready/", views.ready_view, name="ready"),
    # path("start/", views.start_view, name="start"),
    # path("observe/", views.observe_view, name="observe"),
    # path("<str:room_name>/", views.by_name_view, name="by_name"),
]
