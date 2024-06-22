import uuid
from .game import Game


# Game class의 싱글톤 패턴 적용
class RoomManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RoomManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.rooms = {}
            cls._instance.room_id = 0
        return cls._instance

    async def create_game(self, game_type, matched_users):
        try:
            # room_id = uuid.uuid4().int
            # if self.room_id in self.rooms:
            #     logger.warning(f"Room ID {self.room_id} already exists")
            #     return None
            # matched_user = (uid, channel_name, nickname)
            self.room_id += 1
            self.rooms[self.room_id] = await Game.create(
                self.room_id, game_type, matched_users
            )
            print(f"Game created with room_id: {self.room_id}")
            return self.room_id
        except Exception as e:
            print(f"Error starting game: {e}")
            raise

    def get_game_instance(self, room_id):
        if room_id not in self.rooms:
            # error
            print(f"Room ID {room_id} not found")
            return None
        return self.rooms[room_id]

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]
            print(f"Room ID {room_id} removed")
        else:
            print(f"Room ID {room_id} not found")
