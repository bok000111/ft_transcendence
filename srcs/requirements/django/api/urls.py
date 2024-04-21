from django.urls import path

from user import views as user_views

# from pong import views as pong_views

urlpatterns = [
    # /api/ TODO: user/views.py 작성
    path("signup/", user_views.signup_view, name="signup"),
    path("login/", user_views.login_view, name="login"),
    path("logout/", user_views.logout_view, name="logout"),
    # /api/pong/ TODO: pong/views.py 작성
    # path("create/", pong_views.create, name="create"),  # 게임 생성
    # path("join/", pong_views.join, name="join"),  # 게임 참가
    # path(
    # "leave/", pong_views.leave, name="leave"
    # ),  # 게임 나가기 - 새로고침 시 바로 나가지지 않도록 요청으로 분리
]
