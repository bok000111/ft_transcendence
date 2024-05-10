import json
from inspect import iscoroutinefunction
from functools import wraps

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from channels.db import database_sync_to_async

from lobby.models import GameLobby, PlayerInLobby


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
        elif isinstance(obj, GameLobby):
            return {
                "id": obj.pk,
                "name": obj.name,
                "players": [
                    {"id": player.pk, "username": player.username}
                    for player in obj.players.all()
                ],
                "player_count": obj.player_count,
                "max_players": obj.max_players,
                "end_score": obj.end_score,
            }
        elif isinstance(obj, PlayerInLobby):
            return {
                "id": obj.player.pk,
                "score": obj.score,
                "is_host": obj.is_host,
                "is_ready": obj.is_ready,
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
                        "data": {"content_type": "Invalid content type"},
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
                        "data": {"content_type": "Invalid content type"},
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
                "data": {"auth": "Authentication required"},
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
                    return self.jsend_bad_request({"message": "Invalid content type"})
                try:
                    request.json = json.loads(request.body)
                except json.JSONDecodeError:
                    return self.json_response_bad_request({"message": "Invalid body"})
        return await super().dispatch(request, *args, **kwargs)

    def json_response(self, data, **kwargs):
        return JsonResponse(data, **kwargs)

    @database_sync_to_async
    def ajson_response(self, data, **kwargs):
        return self.json_response(data, **kwargs)

    def jsend_ok(self, data, **kwargs):
        return JsonResponse({"status": "success", **data}, status=200, **kwargs)

    @database_sync_to_async
    def ajsend_ok(self, data, **kwargs):
        return self.jsend_ok(data, **kwargs)

    def jsend_created(self, data, **kwargs):
        return JsonResponse({"status": "success", **data}, status=201, **kwargs)

    @database_sync_to_async
    def ajsend_created(self, data, **kwargs):
        return self.jsend_created(data, **kwargs)

    def jsend_bad_request(self, data, **kwargs):
        return JsonResponse({"status": "fail", **data}, status=400, **kwargs)

    @database_sync_to_async
    def ajsend_bad_request(self, data, **kwargs):
        return self.jsend_bad_request(data, **kwargs)

    def jsend_unauthorized(self):
        return JsonResponse(
            {
                "status": "fail",
                "data": {"auth": "Authentication required"},
            },
            status=401,
        )

    @database_sync_to_async
    def ajsend_unauthorized(self):
        return self.jsend_unauthorized()

    def jsend_forbidden(self):
        return JsonResponse(
            {"status": "fail", "data": {"auth": "Forbidden"}}, status=403
        )

    @database_sync_to_async
    def ajsend_forbidden(self):
        return self.jsend_forbidden()

    def jsend_not_found(self, data, **kwargs):
        return JsonResponse({"status": "fail", **data}, status=404, **kwargs)

    @database_sync_to_async
    def ajsend_not_found(self, data, **kwargs):
        return self.jsend_not_found(data, **kwargs)

    def jsend_internal_error(self):
        return JsonResponse(
            {"status": "error", "message": "Internal server error"}, status=500
        )

    @database_sync_to_async
    def ajsend_internal_error(self):
        return self.jsend_internal_error()
