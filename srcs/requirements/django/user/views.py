from api.utils import JsonMixin, JsonAuthRequiredMixin
from user.forms import UserCreateModelForm, UserLoginForm

from django.contrib.auth import authenticate, login, logout
from django.views import View


class SignUpView(JsonMixin, View):
    def post(self, request):
        form = UserCreateModelForm(request.json)
        if form.is_valid():
            new_user = form.save()
            return self.jsend_created({"user": new_user}, "user created")
        return self.jsend_bad_request(
            form.errors.as_json(escape_html=True), "invalid data"
        )


class LoginView(JsonMixin, View):
    def post(self, request):
        if request.user.is_authenticated:
            return self.jsend_bad_request(
                {"auth": "already logged in"}, "already logged in"
            )
        form = UserLoginForm(request.json)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return self.jsend_ok({"user": user}, "logged in")
        return self.jsend_bad_request(
            {"auth": "invalid credentials"}, "invalid credentials"
        )


class LogoutView(JsonMixin, JsonAuthRequiredMixin, View):
    def post(self, request):
        logout(request)

        return self.jsend_ok(None, "logged out")


class MyInfoView(JsonMixin, JsonAuthRequiredMixin, View):
    def get(self, request):
        return self.jsend_ok({"user": request.user}, "user info")


# Path: srcs/requirements/django/user/models.py
