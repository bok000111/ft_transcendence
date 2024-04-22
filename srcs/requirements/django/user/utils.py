from django.http import JsonResponse
from functools import wraps
from inspect import iscoroutinefunction


def need_auth(view):
    if iscoroutinefunction(view):

        @wraps(view)
        async def _wrapped_view(request, *args, **kwargs):
            if not (await request.auser()).is_authenticated:
                return JsonResponse({"message": "Not logged in."}, status=403)
            return await view(request, *args, **kwargs)

        return _wrapped_view

    else:

        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"message": "Not logged in."}, status=403)
            return view(request, *args, **kwargs)

        return _wrapped_view


def need_not_auth(view):
    if iscoroutinefunction(view):

        @wraps(view)
        async def _wrapped_view(request, *args, **kwargs):
            if (await request.auser()).is_authenticated:
                return JsonResponse({"message": "Already logged in."}, status=403)
            return await view(request, *args, **kwargs)

        return _wrapped_view

    else:

        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return JsonResponse({"message": "Already logged in."}, status=403)
            return view(request, *args, **kwargs)

        return _wrapped_view
