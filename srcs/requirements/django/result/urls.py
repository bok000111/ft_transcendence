from django.urls import path
from result.views import TournamentResultView

urlpatterns = [
    path("", TournamentResultView.as_view(), name="result"),
]
