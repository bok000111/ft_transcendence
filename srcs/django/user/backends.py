# backends.py

from user.utils import generate_jwt, auth_token, verify_jwt
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthBackend(BaseBackend):
    def authenticate(self, request=None, **credentials):
        if credentials.get("access"):
            return verify_jwt(credentials["access"])
        if credentials.get("refresh"):
            # TODO: Refresh Token 유효성 검사 및 새로운 Access Token 발급 로직 추가
            return None
        if credentials.get("email") and credentials.get("password"):
            try:
                user = User.objects.get(email=credentials["email"])
            except User.DoesNotExist:
                return None
            if user.check_password(credentials["password"]):
                return user
        if request and request.user.is_authenticated:
            return request.user
        return None

    def login(self, request, user) -> None:
        """
        Create a new Refresh Token and Access Token
        """
        if user.is_anonymous:
            return None

        if (refresh_token := request.COOKIES.get("refresh_token", None)) is not None:
            token_user = auth_token(refresh_token)
            if token_user:
                # TODO: blacklist refresh token and access token
                pass
        request.COOKIES["access_token"] = generate_jwt(user)
        request.COOKIES["refresh_token"] = generate_jwt(user, is_refresh=True)
        return None

    def logout(self, request):
        """
        TODO: blacklist access token and refresh token
        delete refresh token from db and session cookie
        """
        deprecated_access_token = request.COOKIES.get("refresh_token", None)
        deprecated_refresh_token = request.COOKIES.get("refresh_token", None)
        # TODO: blacklist deprecated_tokens
        request.COOKIES["access_token"] = None
        request.COOKIES["refresh_token"] = None
        return None

    # TODO: 만들긴 해야함
    def get_user(self, user_id):
        return None
