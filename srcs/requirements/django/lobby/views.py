from django.views.generic import View

from channels.db import database_sync_to_async

from api.utils import AJsonMixin, AJsonAuthRequiredMixin

from .models import GameLobby, PlayerInLobby
from .forms import LobbyCreateModelForm, NicknameForm


class GameLobbyView(AJsonMixin, AJsonAuthRequiredMixin, View):
    # get lobby list
    async def get(self, request):
        lobbies = await database_sync_to_async(list)(GameLobby.objects.all())
        if not lobbies:
            return self.jsend_ok({"lobbies": []}, "lobbies")
        return await self.ajsend_ok({"lobbies": lobbies}, "lobbies")

    # create lobby
    async def post(self, request):
        form = LobbyCreateModelForm(request.json, user=(user := await request.auser()))
        if form.is_valid():
            new_lobby = await form.asave()
            return await self.ajsend_created({"lobby": new_lobby}, "lobby created")
        else:
            return self.jsend_bad_request(
                form.errors.as_json(escape_html=True), "invalid data"
            )


class GameLobbyDetailView(AJsonMixin, AJsonAuthRequiredMixin, View):
    # get lobby detail
    async def get(self, request, id):
        if id is None:
            return self.jsend_bad_request(None, "invalid data")

        try:
            lobby = await GameLobby.objects.aget(id=id)
        except GameLobby.DoesNotExist:
            return self.jsend_not_found(None, "lobby not found")
        else:
            return await self.ajsend_ok({"lobby": lobby}, "lobby found")

    # join lobby
    async def post(self, request, id):
        if id is None:
            return self.jsend_bad_request(None, "invalid data")

        nickname_form = NicknameForm(request.json)
        if nickname_form.is_valid():
            nickname = nickname_form.cleaned_data["nickname"]
        else:
            return self.jsend_bad_request(
                nickname_form.errors.as_json(), "invalid nickname"
            )

        try:
            lobby = await GameLobby.objects.aget(id=id)
        except GameLobby.DoesNotExist:
            return self.jsend_not_found(None, "lobby not found")

        if await lobby.is_full:
            return self.jsend_bad_request(None, "lobby is full, cannot join lobby")
        elif await database_sync_to_async(
            PlayerInLobby.objects.filter(user=(user := await request.auser())).exists
        )():
            return self.jsend_bad_request(None, "already in lobby")
        elif await database_sync_to_async(
            PlayerInLobby.objects.filter(lobby=lobby, nickname=nickname).exists
        )():
            return self.jsend_bad_request(None, "nickname is already in use")

        await lobby.join(user, nickname=nickname)
        return self.jsend_ok(None, "joined lobby")

    # if the user is the host, delete the lobby
    # if the user is not the host, leave the lobby
    async def delete(self, request, id):
        if id is None:
            return self.jsend_bad_request(None, "invalid data")
        elif (
            lobby := await database_sync_to_async(
                GameLobby.objects.filter(id=id).first
            )()
        ) is None:
            return self.jsend_not_found(None, "lobby not found")
        elif (
            player := await database_sync_to_async(
                PlayerInLobby.objects.filter(
                    lobby=lobby, user=(user := await request.auser())
                ).first
            )()
        ) is None:
            return self.jsend_bad_request(None, "not in lobby")

        if player.is_host:
            await database_sync_to_async(lobby.delete)()
            return self.jsend_ok(None, "lobby deleted")
        else:
            await lobby.leave(user)
            return self.jsend_ok(None, "left lobby")
