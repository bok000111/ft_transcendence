from django.urls import path, include

from user import views as user_views

urlpatterns = [
    # /api/ TODO: user/views.py 작성
    path("signup/", user_views.signup_view, name="signup"),
    path("login/", user_views.login_view, name="login"),
    path("logout/", user_views.logout_view, name="logout"),
    # /api/pong/ TODO: pong/views.py 작성
    path("pong/", include("pong.urls")),
]
