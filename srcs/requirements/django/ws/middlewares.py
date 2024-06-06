# middlewares.py

from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from channels.security.websocket import AllowedHostsOriginValidator


class AuthReqMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        user = scope.get("user")
        if user is None or user.is_anonymous:
            await send({"type": "websocket.close", "code": 4001})
            return
        return await super().__call__(scope, receive, send)


def AuthReqMiddlewareStack(inner):
    return AllowedHostsOriginValidator(AuthMiddlewareStack(AuthReqMiddleware(inner)))
