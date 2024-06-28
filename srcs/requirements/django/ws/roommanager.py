import uuid
from ws.game import Game
from ws.enums import GameType


# 싱글톤 패턴 적용
class RoomManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self._initialized = True
        self.rooms = {}
        self.room_id = 0

    async def create_game(self, game_type, matched_users):
        try:
            # uuid의 int값을 사용하여 room_id 생성(범위 제한, overflow 방지)

            room_id = uuid.uuid4().int & (1 << 32) - 1  # 32비트 정수로 변환
            if room_id in self.rooms:
                print(f"Warning: Room ID {room_id} already exists")
                return None
            # matched_user = (uid, channel_name, nickname)
            self.rooms[room_id] = await Game.create(room_id, game_type, matched_users)

            return room_id

        except Exception as e:
            print(f"Warning: Error starting game: {e}")
            raise

    def get_game_instance(self, room_id):
        if room_id not in self.rooms:
            # error
            print(f"Warning: Room ID {room_id} not found")
            return None
        return self.rooms[room_id]

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]
            print(f"Info: Room ID {room_id} removed")
        else:
            print(f"Warning: Room ID {room_id} not found")

    async def start_game(self, game_type, matched_users):
        gid = await self.create_game(game_type, matched_users)
        if gid is None:
            print("Failed to create game")
            return None
        game = self.rooms[gid]
        if game is None:
            print("Failed to get game instance")
            return None

        await game.start()
        return gid
