from user import views
from django.urls import path


urlpatterns = [
    path("signup/", views.sign_up_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("me/", views.my_info_view, name="myinfo"),
    path("refresh/", views.refresh_token_view, name="refresh"),
    path("csrf/", views.csrf_view, name="csrf"),
    path("2fa/", views.verify_code, name="verify"),
]
