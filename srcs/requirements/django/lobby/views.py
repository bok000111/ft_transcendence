import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View

# from django.http import JsonResponse

# from django.db.utils import IntegrityError
# from django.utils.decorators import method_decorator
from channels.db import database_sync_to_async

from asgiref.sync import sync_to_async


from user.utils import need_auth
from api.utils import need_json, AJsonMixin, AJsonAuthRequiredMixin

from .models import GameLobby, PlayerInLobby
from .forms import LobbyCreateModelForm


class GameLobbyView(AJsonMixin, AJsonAuthRequiredMixin, View):
    # get lobby list
    async def get(self, request):
        lobbies = GameLobby.objects.all()
        if not await database_sync_to_async(lobbies.exists)():
            return self.jsend_not_found({"message": "No lobbies"})
        return await self.ajsend_ok(
            {"message": "Lobbies", "data": {"lobbies": lobbies}}
        )

    # create lobby
    async def post(self, request):
        form = LobbyCreateModelForm(request.json, user=(user := await request.auser()))
        if form.is_valid():
            new_lobby = await form.asave()
            return await self.ajsend_created(
                {"message": "Lobby created", "data": {"lobby": new_lobby}}
            )
        else:
            return self.jsend_bad_request(
                {
                    "message": "Invalid data",
                    "data": form.errors.as_json(),
                }
            )


class GameLobbyDetailView(AJsonMixin, AJsonAuthRequiredMixin, View):
    # get lobby detail
    async def get(self, request, id):
        if id is None:
            return self.jsend_bad_request({"message": "Invalid data"})

        try:
            lobby = await GameLobby.objects.aget(id=id)
        except GameLobby.DoesNotExist:
            return self.jsend_not_found({"message": "Not found"})
        else:
            return await self.ajsend_ok({"message": "Lobby", "data": {"lobby": lobby}})

    # join lobby
    async def post(self, request, id):
        if id is None:
            return self.jsend_bad_request({"message": "Invalid data"})

        try:
            lobby = await GameLobby.objects.aget(id=id)
        except GameLobby.DoesNotExist:
            return self.jsend_not_found({"message": "Not found"})

        if await lobby.is_full:
            return self.jsend_bad_request({"message": "Lobby is full"})
        elif await database_sync_to_async(
            lobby.players.filter(id=(user := await request.auser()).id).exists
        )():
            return self.jsend_bad_request({"message": "Already in the lobby"})
        else:
            await lobby.join(user)
            return self.jsend_ok({"message": "Joined lobby"})

    # if the user is the host, delete the lobby
    # if the user is not the host, leave the lobby
    async def delete(self, request, id):
        if id is None:
            return self.jsend_bad_request({"message": "Invalid data"})

        try:
            lobby = await GameLobby.objects.aget(id=id)
        except GameLobby.DoesNotExist:
            return self.jsend_not_found({"message": "Not found"})

        try:
            player = await PlayerInLobby.objects.aget(
                lobby=lobby, user=(user := await request.auser())
            )
        except lobby.players.model.DoesNotExist:
            return self.jsend_bad_request({"message": "Not in the lobby"})

        if player.is_host:
            await database_sync_to_async(lobby.delete)()
            return self.jsend_ok({"message": "Lobby deleted"})
        else:
            await lobby.leave(user)
            return self.jsend_ok({"message": "Left lobby"})
