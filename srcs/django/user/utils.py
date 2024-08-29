# utils.py

import time
import jwt

from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


def generate_jwt(user, is_refresh=False):
    iat = time.time()
    return jwt.encode(
        {
            "user_id": user.pk,
            "iat": iat,
            "exp": iat
            + (
                settings.JWT_REFRESH_TOKEN_LIFETIME
                if is_refresh
                else settings.JWT_ACCESS_TOKEN_LIFETIME
            ),
            "type": "refresh" if is_refresh else "access",
        },
        settings.SECRET_KEY,
        settings.JWT_ALGORITHM,
    )


def decode_token_to_uid(token, is_refresh=False) -> int | None:
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
        if payload.get("type") != ("refresh" if is_refresh else "access"):
            return None
        user_id = int(payload.get("user_id"))
        return user_id
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass
    except ValueError:
        pass
    except TypeError:
        pass
    return None


def reissue_token(refresh_token):
    if (user_id := decode_token_to_uid(refresh_token, "refresh")) is not None:
        user = User.objects.filter(pk=user_id).first()
        if user is not None:
            user.change_access_token(generate_jwt(user, is_refresh=False))
            return user
    return None


@database_sync_to_async
def areissue_token(refresh_token):
    return reissue_token(refresh_token)


def get_user(token, is_refresh=False):
    if (user_id := decode_token_to_uid(token, is_refresh)) is not None:
        user = User.objects.filter(pk=user_id).first()
        if user is None:
            return AnonymousUser()
        return user
    return AnonymousUser()


@database_sync_to_async
def aget_user(token, is_refresh=False):
    return get_user(token, is_refresh)
