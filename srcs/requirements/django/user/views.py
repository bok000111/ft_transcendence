import json
from asgiref.sync import sync_to_async

from django.conf import settings
from django.contrib.auth import aauthenticate, alogin, alogout, get_user_model
from django.views import View
from django.views.decorators.http import require_http_methods
from channels.db import database_sync_to_async

from api.utils import need_json, AJsonMixin, JsonResponse
from user.utils import need_auth

from .forms import UserCreateModelForm, UserLoginForm

User = get_user_model()


class SignUpView(AJsonMixin, View):
    async def post(self, request):
        form = UserCreateModelForm(request.json)
        if await sync_to_async(form.is_valid)():
            new_user = await database_sync_to_async(form.save)()
            return await self.ajsend_created(
                {
                    "message": "User created",
                    "data": {"user": new_user},
                }
            )
        else:
            return self.jsend_bad_request(
                {
                    "message": "Invalid data",
                    "data": form.errors.as_json(),
                }
            )


class LoginView(AJsonMixin, View):
    async def post(self, request):
        if (await request.auser()).is_authenticated:
            return self.jsend_bad_request({"message": "Already logged in"})
        form = UserLoginForm(request.json)
        if await sync_to_async(form.is_valid)():
            user = await aauthenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                await alogin(request, user)
                return await self.ajsend_ok(
                    {"message": "Logged in", "data": {"user": user}}
                )
        return self.jsend_bad_request({"message": "Invalid credentials"})


@require_http_methods(["POST"])
@need_auth
@need_json
async def logout_view(request):
    await alogout(request)

    return JsonResponse({"message": "Logged out"}, status=200)


# Path: srcs/requirements/django/user/models.py
