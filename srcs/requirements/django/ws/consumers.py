import asyncio
from ws.enums import WebSocketActionType, GameType
from ws.queue import GameQueue
from ws.lobby import Lobby
from ws.game import Game
from ws.roommanager import RoomManager
from ws.tournament import Tournament
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model


User = get_user_model()


class MainConsumer(AsyncJsonWebsocketConsumer):
    room_manager = RoomManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lock = asyncio.Lock()
        self.waiting: GameType = None
        self.playing: Game | Tournament = None

    async def connect(self):
        """
        websocket 연결 시 호출
        lock 사용하여 async-safe
        """
        async with self.lock:
            # await self.channel_layer.group_add(f"user_{self.scope["user"].pk}", self.channel_name)
            await self.accept()

    async def disconnect(self, code):
        """
        websocket 연결 해제 시 호출
        """
        async with self.lock:
            # await self.channel_layer.group_discard(f"user_{self.scope["user"].pk}", self.channel_name)
            pass

    async def send_error(self, code: int, message: str):
        await self.send_json(
            {
                "code": code,
                "action": WebSocketActionType.ERROR.value[0],
                "data": {"message": message},
            }
        )

    async def receive_json(self, content, **kwargs):
        """
        websocket 메시지 수신 시 호출

        Args:
            content: 수신한 json 데이터
        Returns:
            None
        """
        try:
            action = WebSocketActionType.from_str(content.get("action"))
        except ValueError:
            await self.send_error(400, "Invalid action")
            return None

        try:
            await self.channel_layer.send(
                self.channel_name,
                {
                    "type": action.type,
                    "message": content.get("data"),
                },
            )
        except AttributeError:
            await self.send_error(400, "Invalid action")

    async def join_queue(self, event):
        try:  # 대충 입력 검증
            game_type = GameType(event["message"]["type"])
            nickname = event["message"]["nickname"]
            uid = self.scope["user"].pk
        except (ValueError, KeyError):
            await self.send_error(400, "Invalid data")
            return None

        async with self.lock:
            await GameQueue().join_queue(game_type, uid, self.channel_name, nickname)

    async def leave_queue(self, event):
        try:  # 대충 입력 검증
            game_type = GameType(event["message"]["type"])
            uid = self.scope["user"].pk
        except (ValueError, KeyError):
            await self.send_error(400, "Invalid data")
            return None

        async with self.lock:
            await GameQueue().leave_queue(game_type, uid, self.channel_name)

    async def wait_queue(self, event):
        await self.send_json(
            {
                "code": 2001,
                "action": "wait",
                "data": event["message"],
            }
        )

    # message:{
    #     "action": "game_input",
    #     "data": {
    #         "game_id": Int,
    #         "nickname": String,
    #         "keyevent": Int
    #     },
    # }
    async def game_input(self, event):
        gid = event["message"]["game_id"]
        game_instance = self.room_manager.get_game_instance(gid)
        if game_instance is None:
            await self.send_error(400, "Invalid game_id")
            return None
        # game_instance에서 nickname에 해당하는 player의 keyevent를 처리
        game_instance.input(event["message"]["nickname"], event["message"]["keyevent"])

    async def game_info(self, event):
        game_status = event["message"]
        data = game_status["data"]
        if data == "info":
            await self.send_json(
                {
                    "code": 4000,  # temp
                    "action": "game",
                    "data": game_status,
                }
            )
        elif data == "result":
            await self.send_json(
                {
                    "code": 4001,  # temp
                    "action": "end",
                    "data": game_status,
                }
            )

    async def test_response(self, event):
        await self.send_json(event["message"])

    async def _test_response(self, event):
        await self.send_json(event["message"])

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
