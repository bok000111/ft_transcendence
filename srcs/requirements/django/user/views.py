from asgiref.sync import sync_to_async

from django.conf import settings
from django.contrib.auth import aauthenticate, alogin, alogout, get_user_model
from django.views import View
from channels.db import database_sync_to_async

from api.utils import AJsonMixin, AJsonAuthRequiredMixin

from .forms import UserCreateModelForm, UserLoginForm

User = get_user_model()


class SignUpView(AJsonMixin, View):
    async def post(self, request):
        form = UserCreateModelForm(request.json)
        if await sync_to_async(form.is_valid)():
            new_user = await database_sync_to_async(form.save)()
            return await self.ajsend_created({"user": new_user}, "user created")
        else:
            return self.jsend_bad_request(
                form.errors.as_json(escape_html=True), "invalid data"
            )


class LoginView(AJsonMixin, View):
    async def post(self, request):
        if (await request.auser()).is_authenticated:
            return self.jsend_bad_request(
                {"auth": "already logged in"}, "already logged in"
            )
        form = UserLoginForm(request.json)
        if await sync_to_async(form.is_valid)():
            user = await aauthenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                await alogin(request, user)
                return await self.ajsend_ok({"user": user}, "logged in")
        return self.jsend_bad_request(
            {"auth": "invalid credentials"}, "invalid credentials"
        )


class LogoutView(AJsonMixin, AJsonAuthRequiredMixin, View):
    async def post(self, request):
        await alogout(request)

        return self.jsend_ok(None, "logged out")


class MyInfoView(AJsonMixin, AJsonAuthRequiredMixin, View):
    async def get(self, request):
        user = await request.auser()
        return await self.ajsend_ok({"user": user}, "user info")


# Path: srcs/requirements/django/user/models.py
