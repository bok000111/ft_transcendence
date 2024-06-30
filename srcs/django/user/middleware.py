from user.utils import reissue_token, get_user

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

JWT_ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY = settings.SECRET_KEY


class JWTAuthMiddleware:
    """
    Middleware for JWT authentication in Django views
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (access_token := self._get_access_token(request)) is not None:
            user = get_user(access_token)
            if user.is_authenticated:
                request.user = user
                request.COOKIES["access_token"] = access_token
                return self.get_response(request)

        if (refresh_token := request.COOKIES.get("refresh_token")) is not None:
            user, access_token = reissue_token(refresh_token)
            if user is not None:
                request.user = user
                request.COOKIES["access_token"] = access_token
                return self.get_response(request)

        request.user = AnonymousUser()
        return self.get_response(request)

    def _get_access_token(self, request):
        if auth_header := request.headers.get("Authorization", None):
            token_type, _, token = auth_header.partition(" ")
            if token_type == "Bearer" and token is not None:
                return token
        return None
