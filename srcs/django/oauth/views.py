import requests
import os

from user.backends import JWTAuthBackend

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.decorators.http import require_GET


@require_GET
def oauth_login(request):
    if request.user.is_authenticated:
        return redirect(f"https://{os.getenv('HOST_NAME')}")
    return redirect(
        f"{settings.OAUTH_42_URL}?client_id={settings.OAUTH_42_CLIENT_ID}"
        f"&redirect_uri={settings.OAUTH_42_REDIRECT_URI}&response_type=code"
    )


@require_GET
def oauth_callback(request):
    if request.user.is_authenticated:
        return redirect(f"https://{os.getenv('HOST_NAME')}")
    code = request.GET.get("code")
    if not code:
        return redirect(f"https://{os.getenv('HOST_NAME')}")

    user_model = get_user_model()

    token_data = {
        "grant_type": "authorization_code",
        "client_id": settings.OAUTH_42_CLIENT_ID,
        "client_secret": settings.OAUTH_42_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.OAUTH_42_REDIRECT_URI,
    }

    response = requests.post(settings.OAUTH_42_TOKEN_URL, data=token_data, timeout=5)
    response_data = response.json()
    if response.status_code != 200:
        return redirect(f"https://{os.getenv('HOST_NAME')}")

    access_token = response_data.get("access_token")
    if not access_token:
        return redirect(f"https://{os.getenv('HOST_NAME')}")

    info_url = "https://api.intra.42.fr/v2/me"

    response = requests.get(
        info_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=5
    )

    if response.status_code != 200:
        return redirect(f"https://{os.getenv('HOST_NAME')}")

    user_data = response.json()
    email = user_data.get("email")
    username = user_data.get("login")

    user = user_model.objects.filter(
        email=email, username=username, is_oauth_user=True
    ).first()
    if user is not None:
        # oauth 사용자가 이미 가입되어 있으면 로그인 처리
        JWTAuthBackend().login(request, user)
    else:
        # oauth 사용자가 가입되어 있지 않으면 회원가입 처리
        try:
            user = user_model.objects.create(
                email=email, username=username, is_oauth_user=True
            )
            user.set_unusable_password()
            user.save()
            JWTAuthBackend().login(request, user)
        except IntegrityError:
            return redirect(f"https://{os.getenv('HOST_NAME')}")

    response = redirect(f"https://{os.getenv('HOST_NAME')}")
    response.set_cookie(
        "refresh_token",
        request.COOKIES.get("refresh_token"),
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    return response
