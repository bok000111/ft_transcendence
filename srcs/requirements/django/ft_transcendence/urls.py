from django.urls import path, include

from ft_transcendence import views


urlpatterns = [
    path("", views.index, name="index"),  # 메인 페이지 - spa로 구현
    path("api/", include("api.urls")),  # api 요청들
    path("oauth/", include("oauth.urls")),  # 42 OAuth 요청들
]
