# import json

# from channels.generic.websocket import AsyncWebsocketConsumer

# from .models import GameRoom, PlayerInGame

# from ws.utils import ws_need_auth


# class AGameRoomConsumer(AsyncWebsocketConsumer):
#     @ws_need_auth
#     async def connect(self):
#         self.user = self.scope["user"]

#         self.room = await GameRoom.objects.aget(
#             id=self.scope["url_route"]["kwargs"]["room_id"]
#         )
#         if not self.room:
#             await self.close(code=404, reason="Room not found")
#             return

#         self.player = await PlayerInGame.objects.aget(
#             player=self.user,
#             room=self.room,
#         )

#         if not self.player:
#             self.send(text_data=json.dumps({"error": "Join the room first"}))
#             await self.close()
#             return

#         await self.channel_layer.group_add(
#             f"ws_game_room_{self.room.id}", self.channel_name
#         )
#         await self.accept()
#         await self.send(
#             text_data=json.dumps({"message": f"Connected to room {self.room.id}"})
#         )

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data=None, bytes_data=None):
#         await self.send(text_data="Hello world!")
