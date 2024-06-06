from django.http import JsonResponse
from functools import wraps
from inspect import iscoroutinefunction


def need_auth(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    "status": "fail",
                    "data": {"auth": "authorization required"},
                    "message": "authorization required",
                },
                status=401,
            )
        return view(request, *args, **kwargs)

    return _wrapped_view


def need_not_auth(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse(
                {
                    "status": "fail",
                    "data": {"auth": "already logged in"},
                    "message": "already logged in",
                },
                status=403,
            )
        return view(request, *args, **kwargs)

    return _wrapped_view
