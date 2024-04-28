import json
from django.conf import settings
from django.contrib.auth import aauthenticate, alogin, alogout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View
from django.utils.decorators import method_decorator
from django.core import serializers

from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


from api.utils import need_json, AJsonMixin, JsonResponse
from user.utils import need_auth, need_not_auth

from .forms import UserCreateModelForm, UserLoginForm

User = get_user_model()


class SignUpView(AJsonMixin, View):
    @csrf_exempt
    async def post(self, request):
        form = UserCreateModelForm(request.json)
        if await sync_to_async(form.is_valid)():
            await database_sync_to_async(form.save)()
            return self.json_response_created({"message": "User created"})
        else:
            return self.json_response_bad_request(
                {
                    "message": "Invalid data",
                    "detail": {k: ", ".join(v) for k, v in form.errors.items()},
                }
            )


class LoginView(AJsonMixin, View):
    @csrf_exempt
    async def post(self, request):
        if (await request.auser()).is_authenticated:
            return self.json_response_forbidden({"message": "Already logged in"})
        form = UserLoginForm(request.json)
        if await sync_to_async(form.is_valid)():
            user = await aauthenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                await alogin(request, user)
                data = json.loads(
                    serializers.serialize("json", [user], fields=("username", "email"))
                )
                return self.json_response_ok(
                    {
                        "message": "Logged in",
                        "data": {"pk": data[0]["pk"], **data[0]["fields"]},
                    }
                )
            else:
                return self.json_response_bad_request(
                    {"message": "Invalid credentials"}
                )
        else:
            return self.json_response_bad_request(
                {
                    "message": "Invalid data",
                    "detail": {k: ", ".join(v) for k, v in form.errors.items()},
                }
            )


@csrf_exempt
@require_http_methods(["POST"])
@need_auth
@need_json
async def logout_view(request):
    await alogout(request)

    return JsonResponse({"message": "Logged out"}, status=200)


# Path: srcs/requirements/django/user/models.py
