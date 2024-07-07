from django.urls import path, include

from result.views import TournamentResultView

urlpatterns = [
    path("user/", include("user.urls")),
    path("result/", TournamentResultView.as_view(), name="result"),
]
