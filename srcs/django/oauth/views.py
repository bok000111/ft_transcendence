import requests

from user.backends import JWTAuthBackend

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import View


@require_GET
def oauth_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    return redirect(
        f"{settings.OAUTH_42_URL}?client_id={settings.OAUTH_42_CLIENT_ID}"
        f"&redirect_uri={settings.OAUTH_42_REDIRECT_URI}&response_type=code"
    )


@require_GET
def oauth_callback(request):
    if request.user.is_authenticated:
        return redirect("/")
    code = request.GET.get("code")
    if not code:
        print("no code")
        return redirect("oauth_login")

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
        return redirect("oauth_login")

    access_token = response_data.get("access_token")
    if not access_token:
        return redirect("oauth_login")

    info_url = "https://api.intra.42.fr/v2/me"

    response = requests.get(
        info_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=5
    )

    if response.status_code != 200:
        return redirect("oauth_login")

    user_data = response.json()
    email = user_data.get("email")
    username = user_data.get("login")

    try:
        user = user_model.objects.get(email=email, username=username, oauth=True)
    except user_model.DoesNotExist:
        user = user_model.objects.create_user(
            email=email, username=username, oauth=True
        )
        user.set_unusable_password()
        user.save()

    JWTAuthBackend().login(request, user)
    response = redirect(f"/#access_token={request.COOKIES.get('access_token')}")
    response.set_cookie("refresh_token", request.COOKIES.get("refresh_token"))
    return response


# @method_decorator(ensure_csrf_cookie, name="dispatch")
# class OauthLoginView(View):
#     ft_auth_url = (f"{settings.OAUTH_42_URL}?client_id={settings.OAUTH_42_CLIENT_ID}"
#                    f"&redirect_uri={settings.OAUTH_42_REDIRECT_URI}&response_type=code")

#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect("index")
#         return redirect(self.ft_auth_url)

# @method_decorator(ensure_csrf_cookie, name="dispatch")
# class OauthCallbackView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect("index")
#         code = request.GET.get("code")
#         if not code:
#             return redirect("oauth_login")

#         user_model = get_user_model()

#         token_data = {
#             "grant_type": "authorization_code",
#             "client_id": settings.OAUTH_42_CLIENT_ID,
#             "client_secret": settings.OAUTH_42_CLIENT_SECRET,
#             "code": code,
#             "redirect_uri": settings.OAUTH_42_REDIRECT_URI,
#         }

#         response = requests.post(
#             settings.OAUTH_42_TOKEN_URL, data=token_data, timeout=5
#         )
#         response_data = response.json()
#         if response.status_code != 200:
#             return redirect("oauth_login")

#         access_token = response_data.get("access_token")
#         if not access_token:
#             return redirect("oauth_login")

#         info_url = "https://api.intra.42.fr/v2/me"

#         response = requests.get(
#             info_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=5
#         )

#         if response.status_code != 200:
#             return redirect("oauth_login")

#         user_data = response.json()
#         email = user_data.get("email")
#         username = user_data.get("login")

#         try:
#             user = user_model.objects.get(
#                 email=email, username=username, oauth=True)
#         except user_model.DoesNotExist:
#             user = user_model.objects.create_user(
#                 email=email, username=username, oauth=True)
#             user.set_unusable_password()
#             user.save()

#         login(request, user)
#         return redirect("index")
