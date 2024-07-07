from django.urls import path, re_path, include

from ft_transcendence.views import index


urlpatterns = [
    path("api/", include("api.urls")),  # api 요청들
    path("oauth/", include("oauth.urls")),  # 42 OAuth 요청들
    re_path(r"^.*$", index, name="index"),  # 메인 페이지 - 나머지 모든 요청은 여기로
]
