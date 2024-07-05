from user.utils import aget_user

from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware


class JWTChannelAuthMiddleware(BaseMiddleware):
    """
    Middleware for JWT authentication in Channels
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        scope = dict(scope)

        for protocol in scope.get("subprotocols", []):
            if protocol.startswith("jwt.access_token."):
                token = protocol[17:]
                scope["access_token"] = token
                scope["user"] = await aget_user(token)
                break
        if scope.get("user") is None:
            scope["user"] = AnonymousUser()
        return await self.inner(scope, receive, send)
