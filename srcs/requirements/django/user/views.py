from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# from asgiref.sync import sync_to_async
import json

from .models import User


# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    data = json.loads(request.body)
    email = data.get("email", None)
    username = data.get("username", None)
    password = data.get("password", None)

    if not email or not username or not password:
        return JsonResponse({"message": "Invalid request."}, status=400)

    try:
        User.objects.create_user(email, username, password)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"message": "User created."}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"message": "Already logged in."}, status=400)

    data = json.loads(request.body)
    email = data.get("email", None)
    password = data.get("password", None)

    if not email or not password:
        return JsonResponse({"message": "Invalid request."}, status=400)

    user = authenticate(request, email=email, password=password)
    if user is None:
        return JsonResponse({"message": "Invalid credentials."}, status=400)

    login(request, user)

    return JsonResponse({"message": "Logged in."}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Not logged in."}, status=400)

    logout(request)

    return JsonResponse({"message": "Logged out."}, status=200)


# Path: srcs/requirements/django/user/models.py
