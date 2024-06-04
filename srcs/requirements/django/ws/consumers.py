import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from enum import Enum
from collections import deque
from channels.db import database_sync_to_async
import asyncio

User = get_user_model()


# normal_2, normal_4, tournament에 대한 ENUM
class RoomType(Enum):
    NORMAL_2 = 0
    NORMAL_4 = 1
    TOURNAMENT = 2
    LOCAL = 3


class WSConsumer(AsyncWebsocketConsumer):
    users_lock = asyncio.Lock()

    # normal_2, normal_4, tournament
    waiting_users = [deque(), deque(), deque()]
    required_users = [2, 4, 4]
    room_ids = [0, 0, 0]
    user_set = set()

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(code=4001, reason="auth required")

        self.user = self.scope["user"]
        await self.accept()

        # 초기 상태는 아무 방에도 속해있지 않음
        self.room_type = None

    async def disconnect(self, close_code):
        if self.room_type is not None:
            async with self.users_lock:
                if self.user in WSConsumer.user_set:
                    WSConsumer.user_set.remove(self.user)
                if self in WSConsumer.waiting_users[self.room_type]:
                    WSConsumer.waiting_users[self.room_type].remove(self)
        await self.close()

    async def receive_json(self, content):
        if "action" in content:
            action = content["action"]

            if action == "join_room":
                room_type = content.get("room_type")
                await self.join_room(room_type)

        else:
            if self.room_type is None:
                await self.close(code=4002, reason="room type required")
            # play game

    async def join_room(self, room_type):
        # room_type은 0~3 사이의 정수여야 함
        if not isinstance(room_type, int) or room_type < 0 or room_type > 3:
            await self.close(code=4003, reason="invalid room_type")

        if self.room_type is not None:
            await self.close(code=4004, reason="already joined room")

        self.room_type = room_type

        if self.room_type == RoomType.LOCAL.value:
            await self.send_json(
                {"action": "ready_to_start", "room_type": self.room_type}
            )
        else:
            await self.join_group(self.room_type)

    async def join_group(self, room_type):
        async with self.users_lock:
            # user_set에 이미 있으면 오류
            if self.user in WSConsumer.user_set:
                await self.close(code=4004, reason="already joined room")
            WSConsumer.waiting_users[room_type].append(self)
            WSConsumer.user_set.add(self.user)
            if (
                len(WSConsumer.waiting_users[room_type])
                >= WSConsumer.required_users[room_type]
            ):
                # 방 생성
                WSConsumer.room_ids[room_type] += 1
                users = [
                    WSConsumer.waiting_users[room_type].popleft()
                    for _ in range(WSConsumer.required_users[room_type])
                ]
                room_name = self.get_room_name(
                    room_type, WSConsumer.room_ids[room_type]
                )
                for user in users:
                    await self.channel_layer.group_add(room_name, user.channel_name)
                    await user.send_json(
                        {
                            "action": "ready_to_start",
                            "room_type": room_type,
                            "group_name": room_name,
                            "user_list": [u.user.username for u in users],
                        }
                    )

    # 방 타입과 id를 받아서 해당 방 이름을 반환
    def get_room_name(self, room_type, room_id):
        match room_type:
            case RoomType.NORMAL_2.value:
                return f"room_normal_2_{room_id}"
            case RoomType.NORMAL_4.value:
                return f"room_normal_4_{room_id}"
            case RoomType.TOURNAMENT.value:
                return f"room_tournament_{room_id}"
