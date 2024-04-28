import json
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.contrib.auth.mixins import AccessMixin
from functools import wraps
from inspect import iscoroutinefunction


class JsonResponseOk(JsonResponse):
    status_code = 200


class JsonResponseCreated(JsonResponse):
    status_code = 201


class JsonResponseBadRequest(JsonResponse):
    status_code = HttpResponseBadRequest.status_code


class JsonResponseUnauthorized(JsonResponse):
    status_code = 401


class JsonResponseForbidden(JsonResponse):
    status_code = HttpResponseForbidden.status_code


class JsonResponseNotFound(JsonResponse):
    status_code = HttpResponseNotFound.status_code


class JsonResponseInternalError(JsonResponse):
    status_code = 500


def need_json(view):
    if iscoroutinefunction(view):

        @wraps(view)
        async def _wrapped_view(request, *args, **kwargs):
            if request.content_type != "application/json":
                return JsonResponseBadRequest(
                    {"status": "fail", "message": "Invalid content type"}
                )
            return await view(request, *args, **kwargs)

        return _wrapped_view

    else:

        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.content_type != "application/json":
                return JsonResponseBadRequest(
                    {"status": "fail", "message": "Invalid content type"}
                )
            return view(request, *args, **kwargs)

        return _wrapped_view


class AJsonAuthRequiredMixin(AccessMixin):
    def handle_no_permission(self):
        return JsonResponseUnauthorized(
            {"status": "fail", "message": "Authentication required"}
        )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AJsonMixin:
    async def dispatch(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return self.json_response_bad_request({"message": "Invalid content type"})
        match request.method:
            case "POST" | "PUT" | "PATCH" | "DELETE":
                try:
                    request.json = json.loads(request.body)
                except json.JSONDecodeError:
                    return self.json_response_bad_request({"message": "Invalid body"})
        return await super().dispatch(request, *args, **kwargs)

    def json_response(self, data, **kwargs):
        return JsonResponse(data, **kwargs)

    def json_response_ok(self, data, **kwargs):
        return JsonResponseOk({"status": "success", **data}, **kwargs)

    def json_response_created(self, data, **kwargs):
        return JsonResponseCreated({"status": "success", **data}, **kwargs)

    def json_response_bad_request(self, data, **kwargs):
        return JsonResponseBadRequest({"status": "fail", **data}, **kwargs)

    def json_response_unauthorized(self, data, **kwargs):
        return JsonResponseUnauthorized({"status": "fail", **data}, **kwargs)

    def json_response_forbidden(self, data, **kwargs):
        return JsonResponseForbidden({"status": "fail", **data}, **kwargs)

    def json_response_not_found(self, data, **kwargs):
        return JsonResponseNotFound({"status": "fail", **data}, **kwargs)

    def json_response_internal_error(self, data, **kwargs):
        return JsonResponseInternalError({"status": "error", **data}, **kwargs)
