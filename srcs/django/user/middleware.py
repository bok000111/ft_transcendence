from user.utils import reissue_token, get_user

from django.contrib.auth.models import AnonymousUser


class JWTAuthMiddleware:
    """
    Middleware for JWT authentication in Django views
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (access_token := self._get_access_token(request)) is not None:
            if (user := get_user(access_token)).is_authenticated:
                user.set_access_token(access_token)
                request.user = user
                return self._handle_response(request)

        if (refresh_token := request.COOKIES.get("refresh_token")) is not None:
            user = reissue_token(refresh_token)
            if user is not None:
                request.user = user
                return self._handle_response(request)

        request.user = AnonymousUser()
        return self._handle_response(request)

    def _get_access_token(self, request):
        if auth_header := request.headers.get("authorization"):
            token_type, _, token = auth_header.partition(" ")
            if token_type == "Bearer" and token is not None:
                return token
        return None

    def _handle_response(self, request):
        response = self.get_response(request)
        # If the access token is modified, set the new access token in the response
        if request.user.is_authenticated is False:
            response.delete_cookie("refresh_token")
            response["X-Access-Token"] = None
        elif request.user.is_access_token_modified:
            response["X-Access-Token"] = request.user.get_access_token()
        return response


# user/middleware.py
