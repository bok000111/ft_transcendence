# backends.py

from user.utils import get_user, generate_jwt
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class JWTAuthBackend(BaseBackend):
    def authenticate(self, request=None, **credentials):
        if credentials.get("access"):
            user = get_user(credentials["access"])
            if user.is_authenticated:
                user.set_access_token(credentials["access"])
                return user
        if credentials.get("refresh"):
            user = get_user(credentials["refresh"], is_refresh=True)
            if user.is_authenticated:
                return user
        if credentials.get("email") and credentials.get("password"):
            user = User.objects.filter(
                email=credentials["email"], is_oauth_user=False
            ).first()
            if user is None:
                return AnonymousUser()
            if user.check_password(credentials["password"]):
                return user
        if request and request.user.is_authenticated:
            return request.user
        return AnonymousUser()

    def login(self, request, user):
        """
        Create a new Refresh Token and Access Token
        """
        request.user = user
        request.COOKIES["refresh_token"] = generate_jwt(user, is_refresh=True)
        request.user.change_access_token(generate_jwt(user, is_refresh=False))

    def logout(self, request):
        request.user = AnonymousUser()
