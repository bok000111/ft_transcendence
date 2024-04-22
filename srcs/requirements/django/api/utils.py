from django.http import JsonResponse
from functools import wraps
from inspect import iscoroutinefunction


def need_json(view):
    if iscoroutinefunction(view):

        @wraps(view)
        async def _wrapped_view(request, *args, **kwargs):
            if request.content_type != "application/json":
                return JsonResponse({"message": "Invalid content type."}, status=400)
            return await view(request, *args, **kwargs)

        return _wrapped_view

    else:

        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.content_type != "application/json":
                return JsonResponse({"message": "Invalid content type."}, status=400)
            return view(request, *args, **kwargs)

        return _wrapped_view
