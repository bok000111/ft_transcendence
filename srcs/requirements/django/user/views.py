from django.http import JsonResponse
from django.contrib.auth import aauthenticate, alogin, alogout, get_user_model
from django.conf import settings
import json

# decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api.utils import need_json
from user.utils import need_auth, need_not_auth

# model
User = get_user_model()


@csrf_exempt
@require_http_methods(["POST"])
@need_json
async def signup_view(request):
    data = json.loads(request.body)
    email = data.get("email", None)
    username = data.get("username", None)
    password = data.get("password", None)

    try:
        user = await User.objects.create_user(
            email=email, username=username, password=password
        )
        return JsonResponse({"message": "User created."}, status=201)
    except ValueError as e:
        return JsonResponse({"message": f"{e}"}, status=400)
    except Exception as e:
        if settings.DEBUG:
            return JsonResponse({"message": f"{e}"}, status=500)
        return JsonResponse({"message": "Something went wrong."}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@need_not_auth
@need_json
async def login_view(request):
    data = json.loads(request.body)
    email = data.get("email", None)
    password = data.get("password", None)

    if not email or not password:
        return JsonResponse({"message": "Invalid request."}, status=400)

    user = await aauthenticate(request, email=email, password=password)
    if user is None:
        return JsonResponse({"message": "Invalid credentials."}, status=400)

    await alogin(request, user)

    return JsonResponse({"message": "Logged in."}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
@need_auth
@need_json
async def logout_view(request):
    await alogout(request)

    return JsonResponse({"message": "Logged out."}, status=200)


# Path: srcs/requirements/django/user/models.py
