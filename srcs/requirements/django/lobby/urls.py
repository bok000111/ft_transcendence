from django.urls import path

from . import views

urlpatterns = [
    path("", views.GameLobbyView.as_view(), name="lobby"),
    path("<int:id>/", views.GameLobbyDetailView.as_view(), name="lobby_detail"),
]
