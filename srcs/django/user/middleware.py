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
            if (user := get_user(access_token)) is not None and user.is_authenticated:
                user.access_token = access_token
                request.user = user
                return self._handle_response(request)

        if (refresh_token := request.COOKIES.get("refresh_token")) is not None:
            user, access_token = reissue_token(refresh_token)
            if user is not None:
                user.access_token = access_token
                user.is_access_token_modified = True
                request.user = user
                return self._handle_response(request)

        request.user = AnonymousUser()
        return self._handle_response(request)

    def _get_access_token(self, request):
        if auth_header := request.headers.get("Authorization", None):
            token_type, _, token = auth_header.partition(" ")
            if token_type == "Bearer" and token is not None:
                return token
        return None

    def _handle_response(self, request):
        response = self.get_response(request)
        if getattr(request.user, "is_access_token_modified", False) is True:
            response["X-Access-Token"] = request.user.access_token
        return response
