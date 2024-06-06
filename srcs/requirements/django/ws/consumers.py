from asyncio import Queue

from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from ws.enums import WebSocketActionType, GameType

User = get_user_model()


class MainConsumer(AsyncJsonWebsocketConsumer):
    queue = {
        GameType.NORMAL_2: Queue(),
        GameType.NORMAL_4: Queue(),
        GameType.TOURNAMENT: Queue(),
    }

    async def connect(self):
        self.waiting = None
        self.playing = None  # 관리 방법은 바뀔 수 있음

        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive_json(self, content):
        match WebSocketActionType(content.get("action")):
            case WebSocketActionType.JOIN:
                await self.channel_layer.send(
                    self.channel_name,
                    {
                        "type": "join.queue",
                        "message": content.get("data"),
                    },
                )
            case WebSocketActionType.LEAVE:
                pass
            case WebSocketActionType.GAME_INPUT:
                pass
            case WebSocketActionType.ME:
                pass
            case WebSocketActionType.ERROR:
                pass
            case _:  # WebSocketActionType.NONE or unknown
                pass

    async def send_error(self, code, message):
        await self.send_json(
            {
                "code": code,
                "action": WebSocketActionType.ERROR.value,
                "data": {"message": message},
            }
        )

    async def join_queue(self, event):
        if self.waiting is not None or self.playing is not None:
            await self.send_error(4001, "already joined")
            return
        message = event.get("message")
        if message is None:
            await self.send_error(4000, "message required")

        game_type = message.get("type")
        if type is None:
            await self.send_error(4000, "game_type required")
            return
        game_type = GameType(game_type)

        nickname = message.get("nickname")
        if nickname is None:
            await self.send_error(4000, "nickname required")

        if game_type not in self.queue:
            await self.send_json(
                {
                    "action": WebSocketActionType.WAIT.value,
                    "data": {"message": "미구현, 로컬은 대기열 없이 바로 시작"},
                }
            )
        self.waiting = game_type
        await self.queue[game_type].put({self.scope["user"].pk, nickname})

        await self.channel_layer.group_add(
            f"queue_{game_type.value}",
            self.channel_name,
        )

        await self.channel_layer.group_send(
            f"queue_{game_type.value}",
            {
                "type": "queue.size",
                "size": self.queue[game_type].qsize(),
            },
        )

        if self.queue[game_type].qsize() >= GameType.max_player(game_type):
            print("game start")
            # game start
            pass

    async def queue_size(self, event):
        await self.send_json(
            {
                "action": WebSocketActionType.WAIT.value,
                "data": {"waiting_users": event["size"]},
            }
        )

    #     if "action" in content:
    #         action = content["action"]

    #         if action == "join_room":
    #             room_type = content.get("room_type")
    #             await self.join_room(room_type)

    #     else:
    #         if self.room_type is None:
    #             await self.close(code=4002, reason="room type required")
    #         # play game

    # async def join_room(self, room_type):
    #     # room_type은 0~3 사이의 정수여야 함
    #     if not isinstance(room_type, int) or room_type < 0 or room_type > 3:
    #         await self.close(code=4003, reason="invalid room_type")

    #     if self.room_type is not None:
    #         await self.close(code=4004, reason="already joined room")

    #     self.room_type = room_type

    #     if self.room_type == RoomType.LOCAL.value:
    #         await self.send_json(
    #             {"action": "ready_to_start", "room_type": self.room_type}
    #         )
    #     else:
    #         await self.join_group(self.room_type)

    # async def join_group(self, room_type):
    #     async with self.users_lock:
    #         # user_set에 이미 있으면 오류
    #         if self.user in WSConsumer.user_set:
    #             await self.close(code=4004, reason="already joined room")
    #         WSConsumer.waiting_users[room_type].append(self)
    #         WSConsumer.user_set.add(self.user)
    #         if (
    #             len(WSConsumer.waiting_users[room_type])
    #             >= WSConsumer.required_users[room_type]
    #         ):
    #             # 방 생성
    #             WSConsumer.room_ids[room_type] += 1
    #             users = [
    #                 WSConsumer.waiting_users[room_type].popleft()
    #                 for _ in range(WSConsumer.required_users[room_type])
    #             ]
    #             room_name = self.get_room_name(
    #                 room_type, WSConsumer.room_ids[room_type]
    #             )
    #             for user in users:
    #                 await self.channel_layer.group_add(room_name, user.channel_name)
    #                 await user.send_json(
    #                     {
    #                         "action": "ready_to_start",
    #                         "room_type": room_type,
    #                         "group_name": room_name,
    #                         "user_list": [u.user.username for u in users],
    #                     }
    #                 )

    # # 방 타입과 id를 받아서 해당 방 이름을 반환
    # def get_room_name(self, room_type, room_id):
    #     match room_type:
    #         case RoomType.NORMAL_2.value:
    #             return f"room_normal_2_{room_id}"
    #         case RoomType.NORMAL_4.value:
    #             return f"room_normal_4_{room_id}"
    #         case RoomType.TOURNAMENT.value:
    #             return f"room_tournament_{room_id}"
