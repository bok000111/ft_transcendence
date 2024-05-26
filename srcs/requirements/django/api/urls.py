from django.urls import path, include


urlpatterns = [
    path("user/", include("user.urls")),
    path("lobby/", include("lobby.urls")),
    # path("pong/", include("pong.urls")),
]
