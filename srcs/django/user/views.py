import json
from api.utils import JsendResponse
from user.forms import UserCreateModelForm, UserLoginForm
from user.backends import JWTAuthBackend

from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@require_POST
def sign_up_view(request):
    if request.content_type != "application/json":
        return JsendResponse(
            {"errors": "invalid content type"},
            message="invalid content type",
            status=400,
        )
    if request.user.is_authenticated:
        return JsendResponse(
            {"auth": "already logged in"}, message="already logged in", status=400
        )
    try:
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsendResponse(
            {"errors": "invalid json"}, message="invalid json", status=400
        )
    form = UserCreateModelForm(json_data)
    if form.is_valid():
        try:
            new_user = form.save()
        except IntegrityError:
            return JsendResponse(
                {"errors": "email already exists"},
                message="email already exists",
                status=400,
            )
        return JsendResponse({"user": new_user}, message="user created", status=201)
    return JsendResponse({"errors": form.errors}, message="bad request", status=400)


@require_POST
def login_view(request):
    if request.content_type != "application/json":
        return JsendResponse(
            {"errors": "invalid content type"},
            message="invalid content type",
            status=400,
        )
    if request.user.is_authenticated:
        return JsendResponse(
            {"user": request.user}, message="already logged in", status=200
        )

    try:
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsendResponse(
            {"errors": "invalid json"}, message="invalid json", status=400
        )
    form = UserLoginForm(json_data)
    if form.is_valid():
        user = JWTAuthBackend().authenticate(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        if user.is_anonymous:
            return JsendResponse(
                {"auth": "invalid credentials"},
                message="invalid credentials",
                status=400,
            )

        if user.send_otp_code() is False:
            return JsendResponse(
                {"auth": "failed to send code"},
                message="failed to send code",
                status=400,
            )
        return JsendResponse(
            {"user": user},
            status=200,
        )
    return JsendResponse(
        {"auth": "invalid credentials"},
        message="invalid credentials",
        status=400,
    )


@require_POST
def logout_view(request):
    if request.content_type != "application/json":
        return JsendResponse({"errors": "invalid content type"}, status=400)
    if request.user.is_anonymous:
        return JsendResponse({"auth": "not logged in"}, status=401)

    JWTAuthBackend().logout(request)

    response = JsendResponse(None, status=200)
    response.delete_cookie("refresh_token")
    return response


@require_GET
@ensure_csrf_cookie
def my_info_view(request):
    if request.user.is_anonymous:
        return JsendResponse({"user": None}, message="not logged in", status=200)
    return JsendResponse({"user": request.user}, status=200)


@require_POST
def refresh_token_view(request):
    if request.content_type != "application/json":
        return JsendResponse({"errors": "invalid content type"}, status=400)
    if request.user.is_anonymous:
        return JsendResponse({"auth": "not logged in"}, status=401)

    # 재발급은 미들웨어에서 처리해서 바로 보내면 됨
    return JsendResponse({}, message="ok", status=200)


@require_POST
def verify_code(request):
    if request.content_type != "application/json":
        return JsendResponse({"errors": "invalid content type"}, status=400)
    if request.user.is_authenticated:
        return JsendResponse({"auth": "already logged in"}, status=400)

    try:
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsendResponse(
            {"errors": "invalid json"}, message="invalid json", status=400
        )
    code = json_data.get("code")

    if (user := User.verify_otp_code(code)) is None:
        return JsendResponse({"auth": "invalid code"}, status=400)

    JWTAuthBackend().login(request, user)
    refresh_token = request.COOKIES.get("refresh_token")
    response = JsendResponse({"user": user}, status=200)
    response.set_cookie(
        "refresh_token", refresh_token, secure=True, httponly=True, samesite="Lax"
    )
    return response
