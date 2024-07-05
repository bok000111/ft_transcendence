import json
from functools import wraps

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet


class ModelJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return tuple(o)
        if isinstance(o, get_user_model()):
            return {
                "id": o.pk,
                "username": o.username,
                "email": o.email,
            }
        if hasattr(o, "as_dict"):
            return o.as_dict()
        return super().default(o)


class CustomJsonResponse(JsonResponse):
    def __init__(self, data, encoder=ModelJSONEncoder, **kwargs):
        super().__init__(data, encoder=encoder, **kwargs)


def need_json(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.content_type != "application/json":
            return CustomJsonResponse(
                {
                    "status": "fail",
                    "data": {"content_type": "invalid content type"},
                    "message": "invalid content type",
                },
                status=400,
            )
        return view(request, *args, **kwargs)

    return _wrapped_view


class JsonAuthRequiredMixin(AccessMixin):
    def handle_no_permission(self):
        return CustomJsonResponse(
            {
                "status": "fail",
                "data": {"auth": "authentication required"},
                "message": "authentication required",
            },
            status=401,
        )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class JsonMixin:
    def dispatch(self, request, *args, **kwargs):
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
        return super().dispatch(request, *args, **kwargs)

    def json_response(
        self, status="success", data=None, message=None, code=200, **kwargs
    ):
        return CustomJsonResponse(
            {"status": status, "data": data, "message": message}, status=code, **kwargs
        )

    def jsend_ok(self, data, message, **kwargs):
        return self.json_response("success", data, message, 200, **kwargs)

    def jsend_created(self, data, message, **kwargs):
        return self.json_response("success", data, message, 201, **kwargs)

    def jsend_bad_request(self, data, message, **kwargs):
        return self.json_response("fail", data, message, 400, **kwargs)

    def jsend_unauthorized(self):
        return self.json_response(
            "fail", {
                "auth": "authorization required"}, "authorization required", 401
        )

    def jsend_forbidden(self):
        return self.json_response("fail", {"auth": "forbidden"}, "forbidden", 403)

    def jsend_not_found(self, data, message, **kwargs):
        return self.json_response("fail", data, message, 404, **kwargs)

    def jsend_internal_error(self):
        return self.json_response("error", None, "internal server error", 500)
