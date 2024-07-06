import asyncio
from ws.enums import WebSocketActionType, GameType
from ws.queue import GameQueue
from ws.lobby import Lobby
from ws.game import Game
from ws.roommanager import RoomManager

# from ws.tournament import Tournament
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class MainConsumer(AsyncJsonWebsocketConsumer):
    room_manager = RoomManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lock = asyncio.Lock()
        self.waiting: GameType | None = None
        self.playing: int | None = None

    async def connect(self):
        """
        websocket 연결 시 호출
        lock 사용하여 async-safe
        """
        await self.accept("jwt.access_token")

    async def disconnect(self, code):
        """
        websocket 연결 해제 시 호출
        """
        # print(f"disconnect / type: {self.waiting}")
        if self.waiting is not None:
            async with self.lock:
                await GameQueue().leave_queue(
                    self.waiting, self.scope["user"].pk, self.channel_name
                )
        else:
            game = self.room_manager.get_game_instance(self.playing)
            if game is not None:
                for player in game.players:
                    if player.uid == self.scope["user"].pk:
                        player.score = -1
                        break
                game.status = "end"

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

        if self.scope["user"].is_anonymous:
            await self.send_error(4001, "Unauthorized")
            return None

        if (action := WebSocketActionType.from_str(content.get("action"))) is None:
            await self.send_error(400, "Invalid action")
            return None

        try:
            if action != WebSocketActionType.GAME_INPUT:
                print(f"action: {action}")
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
        try:
            print(f"join_queue event: {event}")
            game_type = GameType(event["message"]["type"])
            nickname = event["message"]["nickname"]
            uid = self.scope["user"].pk
        except (ValueError, KeyError):
            await self.send_error(400, "Invalid data")
            return None

        async with self.lock:
            self.waiting = game_type
            print(f"uid: {uid}")
            if game_type == GameType.LOCAL:
                matched_users = [
                    (uid, self.channel_name, "player"),
                    (uid, self.channel_name, "player"),
                ]
                await self.room_manager.start_game(game_type, matched_users)
            elif game_type == GameType.AI:
                await self.room_manager.start_game(
                    game_type, [(uid, self.channel_name, "player")]
                )
            else:
                await GameQueue().join_queue(
                    game_type, uid, self.channel_name, nickname
                )

    async def leave_queue(self, event):
        try:
            uid = self.scope["user"].pk
        except (ValueError, KeyError):
            await self.send_error(400, "Invalid data")
            return None

        async with self.lock:
            if (
                self.waiting != GameType.LOCAL
                and self.waiting != GameType.AI
                and self.waiting is not None
            ):
                print(f"game_type: {self.waiting}, {uid}")
                await GameQueue().leave_queue(self.waiting, uid, self.channel_name)
                self.waiting = None

    async def wait_queue(self, event):
        await self.send_json(
            {
                "code": 2001,
                "action": "wait",
                "data": event["message"],
            }
        )

    """
    message:{
        "game_id": Int,
        "nickname": String,
        "keyevent": Int
    }
    """

    async def game_input(self, event):
        gid = event["message"]["game_id"]
        game_instance = self.room_manager.get_game_instance(gid)
        if game_instance is None:
            await self.send_error(400, "Invalid game_id")
            return None
        game_instance.handle_keyevent(
            event["message"]["nickname"], event["message"]["keyevent"]
        )

    async def game_info(self, event):
        game_status = event["message"]
        data_type = event["data_type"]
        async with self.lock:
            if data_type == "info":
                await self.send_json(
                    {
                        "code": 4000,  # temp
                        "action": "game",
                        "data": game_status,
                    }
                )
            elif data_type == "result":
                await self.send_json(
                    {
                        "code": 4001,  # temp
                        "action": "end",
                        "data": game_status,
                    }
                )
                # if game_status["type"] != GameType.SUB_GAME.value:
                #     self.room_manager.remove_room(self.playing)

            elif data_type == "start":
                self.waiting = None
                self.playing = game_status["id"]
                uid = self.scope["user"].pk
                for i in range(len(event["uids"])):
                    if event["uids"][i] == uid:
                        nickname = game_status["users"][i]
                        break
                game_status["my_nickname"] = nickname
                await self.send_json(
                    {
                        "code": 4002,  # temp
                        "action": "start",
                        "data": game_status,
                    }
                )

    async def tournament_info(self, event):
        print("\033[92m" + f"tournament_info: {event}" + "\033[0m")
        info = event["message"]
        uid = self.scope["user"].pk
        for i in range(len(event["uids"])):
            if event["uids"][i] == uid:
                nickname = info["users"][i]
                break
        info["my_nickname"] = nickname
        await self.send_json(
            {
                "code": 4003,  # temp
                "action": "start",
                "data": info,
            }
        )

    async def tournament_result(self, event):
        result = event["message"]
        await self.send_json(
            {
                "code": 4004,  # temp
                "action": "end",
                "data": result,
            }
        )

    async def receive_error(self, event):
        code = int(event["code"])
        message = event["message"]
        await self.send_error(code, message)
