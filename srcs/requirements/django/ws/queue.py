import asyncio
from collections import deque
from ws.enums import GameType
from ws.roommanager import RoomManager
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer


class GameQueue:
    _instance = None  # 싱글톤 인스턴스를 저장할 클래스 변수
    _initialized = False  # 싱글톤 인스턴스 초기화 여부
    User = get_user_model()
    channel_layer = get_channel_layer()

    class _QueueManager:
        def __init__(self):
            self._lock = asyncio.Lock()  # 외부에서 직접 접근하지 않도록 _ 붙임
            self.queue = deque[int]()
            self.dict_ = dict[int, tuple[str, str]]()
            # 파이썬 내부 dict와 겹치지 않도록 _ 붙임

        def __contains__(self, uid: int):
            return uid in self.dict_

        def __len__(self):
            return len(self.queue)

        def append(self, uid: int, channel_name: str, nickname: str):
            self.queue.append(uid)
            self.dict_[uid] = (channel_name, nickname)

        def popleft(self) -> tuple[int, str, str]:
            uid = self.queue.popleft()
            return (uid, *(self.dict_.pop(uid)))

        def remove(self, uid: int):
            self.queue.remove(uid)  # O(n)인데 일단 사용 TODO: 가능하면 개선
            self.dict_.pop(uid)

        async def __aenter__(self):
            await self._lock.acquire()
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            self._lock.release()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._queue_manager = {t: self._QueueManager() for t in GameType}
        self._initialized = True

    # TODO: LOCAL 게임 처리 구현
    async def join_queue(
        self,
        game_type: GameType,
        uid: int,
        channel_name: str,
        nickname: str,
    ) -> None:
        async with self._queue_manager[game_type] as manager:
            if uid in manager:
                return None  # TODO: 이미 대기 중인 경우 에러 보내야함
            manager.append(uid, channel_name, nickname)
            await self.channel_layer.group_add(f"queue_{game_type.name}", channel_name)

            # 대기 중인 유저들에게 대기 중인 유저 수 전송
            await self._notify(game_type)

            while game_type.max_player() <= len(manager):  # 게임 시작 조건
                # 게임 인원수 만큼 매칭
                matched_uids = [
                    manager.popleft() for _ in range(game_type.max_player())
                ]

                # 매칭된 유저들을 대기열에서 제거
                await asyncio.gather(
                    *[
                        self.channel_layer.group_discard(
                            f"queue_{game_type.name}", channel_name
                        )
                        for _, channel_name, _ in matched_uids
                    ],
                )

                # 임시로 그냥 테스트 출력
                matched_users = [
                    (uid, (await self.User.objects.aget(pk=uid)).username, nickname)
                    for uid, _, nickname in matched_uids
                ]
                # print(f"{game_type.name}: {matched_users}")

                # 대충 게임 시작하는 코드 TODO: Game 구현
                room_manager = RoomManager()
                gid = await room_manager.create_game(game_type, matched_uids)
                if gid is None:
                    print("Failed to create game")
                    return None
                game = await room_manager.get_game_instance(gid)
                if game is None:
                    print("Failed to get game instance")
                    return None
                await game.start()

    async def leave_queue(self, game_type: GameType, uid: int, channel_name: str):
        async with self._queue_manager[game_type] as manager:
            if uid not in manager:
                return None  # TODO: 대기 중이 아닌 경우 에러 보내야함
            manager.remove(uid)
            await self.channel_layer.group_discard(
                f"queue_{game_type.name}", channel_name
            )
            # 나가는 유저에게 확인 메시지 전송
            await self.channel_layer.send(
                channel_name,
                {
                    "type": "send_json",
                    "message": {
                        "action": "leave",
                        "data": {
                            "type": game_type.value,
                        },
                    },
                },
            )

            # 대기 중인 유저들에게 대기 중인 유저 수 전송
            await self._notify(game_type)

    async def _notify(self, game_type: GameType):
        await self.channel_layer.group_send(
            f"queue_{game_type.name}",
            {
                "type": "wait.queue",
                "message": {
                    "type": game_type.value,
                    "waiting_users": len(self._queue_manager[game_type]),
                },
            },
        )
