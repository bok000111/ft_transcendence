# utils.py

import jwt
import time
import datetime

from channels.db import database_sync_to_async
from django.conf import settings
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

JWT_REFRESH_TOKEN_LIFETIME = int(settings.JWT_REFRESH_TOKEN_LIFETIME)
JWT_ACCESS_TOKEN_LIFETIME = int(settings.JWT_ACCESS_TOKEN_LIFETIME)


def generate_jwt(user, is_refresh=False):
    iat = datetime.datetime.now(datetime.UTC).timestamp()
    return jwt.encode(
        {
            "user_id": user.pk,
            "iat": iat,
            "exp": iat
            + (JWT_REFRESH_TOKEN_LIFETIME if is_refresh else JWT_ACCESS_TOKEN_LIFETIME),
            "type": "refresh" if is_refresh else "access",
        },
        settings.SECRET_KEY,
        settings.JWT_ALGORITHM,
    )


def auth_token(token, type="access") -> int | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM,
            {
                "verify_exp": True,
                "verify_signature": True,
            },
        )
        if payload.get("type", None) != type:
            return None
        return payload.get("user_id", None)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None


def reissue_token(token, type="refresh"):
    if (user_id := auth_token(token, type)) is not None:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return (None, None)
        return (user, generate_jwt(user, is_refresh=False))
    return (None, None)


@database_sync_to_async
def areissue_token(token, type="refresh"):
    return reissue_token(token, type)


def verify_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload["type"] not in ["access", "refresh"]:
            return None
        if payload["exp"] < int(time.time()):
            return None
        user_id = payload.get("user_id")
        user = User.objects.get(pk=user_id)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None


def refresh_jwt(token):
    user = verify_jwt(token)
    if user:
        return generate_jwt(user, is_refresh=True)
    return None


def get_user(token):
    if (user_id := auth_token(token)) is not None:
        return User.objects.get(pk=user_id)
    return AnonymousUser()


@database_sync_to_async
def aget_user(token):
    if (user_id := auth_token(token)) is not None:
        return User.objects.get(pk=user_id)
    return AnonymousUser()
