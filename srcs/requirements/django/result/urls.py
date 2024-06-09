from django.urls import path
from result import TournamentResultView

urlpatterns = [
    path("result/", TournamentResultView.as_view(), name='result'),
]
