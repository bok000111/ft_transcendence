from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.OauthLoginView.as_view(), name="oauth_login"),
    path("callback/", views.OauthCallbackView.as_view(), name="oauth_callback"),
]
