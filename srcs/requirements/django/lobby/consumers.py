import json

from django.utils.decorators import method_decorator
from channels.generic.websocket import AsyncWebsocketConsumer

from ws.utils import ws_need_auth
from lobby.models import GameLobby, PlayerInLobby


# 일단은 에코 서버로 만들어놓음
@method_decorator(ws_need_auth, name="connect")
class AGameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        try:
            self.lobby = await GameLobby.objects.aget(
                id=self.scope["url_route"]["kwargs"]["lobby_id"]
            )
        except GameLobby.DoesNotExist:
            await self.close(code=404, reason="Room not found")
            return

        try:
            self.player = await PlayerInLobby.objects.aget(
                player=self.user,
                lobby=self.lobby,
            )
        except PlayerInLobby.DoesNotExist:
            await self.close(code=400, reason="Join the room first")
            return

        await self.channel_layer.group_add(
            f"ws_game_lobby_{self.lobby.id}", self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(
            f"ws_game_lobby_{self.lobby.id}",
            {
                "type": "lobby_message",
                "message": f"{self.user.username} has joined the lobby",
            },
        )

    async def disconnect(self, close_code):
        if self.player.is_host:
            await self.lobby.delete()
            await self.channel_layer.group_send(
                f"ws_game_lobby_{self.lobby.id}",
                {
                    "type": "lobby_message",
                    "message": "The host has left the lobby, the lobby has been deleted",
                },
            )
            self.channel_layer.group_discard(
                f"ws_game_lobby_{self.lobby.id}", self.channel_name
            )
        else:
            await self.lobby.leave(self.user)

        await self.channel_layer.group_send(
            f"ws_game_lobby_{self.lobby.id}",
            {
                "type": "left",
                "message": f"{self.user.username} has left the lobby",
            },
        )
        await self.channel_layer.group_discard(
            f"ws_game_lobby_{self.lobby.id}", self.channel_name
        )

    async def receive(self, json_data=None):
        if json_data is None:
            return

        # match json_data.get("command"):
        #     case "ready":
        #         await self.ready(self.user)
        #     case "unready":
        #         await self.lobby.unready(self.user)
        #     case "start":
        #         await self.lobby.start(self.user)
        #     case _:
        #         await self.send(text_data=json.dumps({"error": "Invalid command"}))

        data = json.loads(json_data)

        await self.send(data)
