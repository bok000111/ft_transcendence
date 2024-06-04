import json
from inspect import iscoroutinefunction
from functools import wraps

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from channels.db import database_sync_to_async


User = get_user_model()


class ModelJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return tuple(obj)
        elif isinstance(obj, User):
            return {
                "id": obj.pk,
                "username": obj.username,
                "email": obj.email,
            }
        elif hasattr(obj, "as_dict"):
            return obj.as_dict()
        return super().default(obj)


class JsonResponse(JsonResponse):
    def __init__(self, data, encoder=ModelJSONEncoder, **kwargs):
        super().__init__(data, encoder=encoder, **kwargs)


def need_json(view):
    if iscoroutinefunction(view):

        @wraps(view)
        async def _wrapped_view(request, *args, **kwargs):
            if request.content_type != "application/json":
                return JsonResponse(
                    {
                        "status": "fail",
                        "data": {"content_type": "invalid content type"},
                        "message": "invalid content type",
                    },
                    status=400,
                )
            return await view(request, *args, **kwargs)

        return _wrapped_view

    else:

        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.content_type != "application/json":
                return JsonResponse(
                    {
                        "status": "fail",
                        "data": {"content_type": "invalid content type"},
                        "message": "invalid content type",
                    },
                    status=400,
                )
            return view(request, *args, **kwargs)

        return _wrapped_view


class AJsonAuthRequiredMixin(AccessMixin):
    def handle_no_permission(self):
        return JsonResponse(
            {
                "status": "fail",
                "data": {"auth": "authentication required"},
                "message": "authentication required",
            },
            status=401,
        )

    async def dispatch(self, request, *args, **kwargs):
        if not (await request.auser()).is_authenticated:
            return self.handle_no_permission()
        return await super().dispatch(request, *args, **kwargs)


class AJsonMixin:
    async def dispatch(self, request, *args, **kwargs):
        match request.method:
            case "POST" | "PUT" | "PATCH":
                if request.content_type != "application/json":
                    return self.jsend_bad_request(
                        {"content_type": "invalid content type"}, "invalid content type"
                    )
                try:
                    request.json = json.loads(request.body)
                except json.JSONDecodeError:
                    return self.jsend_bad_request(
                        {"content": "invalid json"}, "invalid json"
                    )
        return await super().dispatch(request, *args, **kwargs)

    def json_response(
        self, status="success", data=None, message=None, code=200, **kwargs
    ):
        return JsonResponse(
            {"status": status, "data": data, "message": message}, status=code, **kwargs
        )

    @database_sync_to_async
    def ajson_response(self, status, data, message, code, **kwargs):
        return self.json_response(status, data, message, code, **kwargs)

    def jsend_ok(self, data, message, **kwargs):
        return self.json_response("success", data, message, 200, **kwargs)

    @database_sync_to_async
    def ajsend_ok(self, data, message, **kwargs):
        return self.jsend_ok(data, message, **kwargs)

    def jsend_created(self, data, message, **kwargs):
        return self.json_response("success", data, message, 201, **kwargs)

    @database_sync_to_async
    def ajsend_created(self, data, message, **kwargs):
        return self.jsend_created(data, message, **kwargs)

    def jsend_bad_request(self, data, message, **kwargs):
        return self.json_response("fail", data, message, 400, **kwargs)

    @database_sync_to_async
    def ajsend_bad_request(self, data, message, **kwargs):
        return self.jsend_bad_request(data, message, **kwargs)

    def jsend_unauthorized(self):
        return self.json_response(
            "fail", {"auth": "authorization required"}, "authorization required", 401
        )

    @database_sync_to_async
    def ajsend_unauthorized(self):
        return self.jsend_unauthorized()

    def jsend_forbidden(self):
        return self.json_response("fail", {"auth": "forbidden"}, "forbidden", 403)

    @database_sync_to_async
    def ajsend_forbidden(self):
        return self.jsend_forbidden()

    def jsend_not_found(self, data, message, **kwargs):
        return self.json_response("fail", data, message, 404, **kwargs)

    @database_sync_to_async
    def ajsend_not_found(self, data, message, **kwargs):
        return self.jsend_not_found(data, message, **kwargs)

    def jsend_internal_error(self):
        return self.json_response("error", None, "internal server error", 500)

    @database_sync_to_async
    def ajsend_internal_error(self):
        return self.jsend_internal_error()
