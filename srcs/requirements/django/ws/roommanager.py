from .game import Game
import logging

logger = logging.getLogger(__name__)


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
            # room_id 임시로 len(self.rooms)로 설정
            # matched_user = (uid, channel_name, nickname)
            self.rooms[self.room_id] = await Game.create(
                self.room_id, game_type, matched_users
            )
            room_id = self.room_id
            self.room_id += 1
            logger.info(f"Game created with room_id: {room_id}")
            return room_id
        except Exception as e:
            logger.error(f"Error starting game: {e}")
            raise

    def get_game_instance(self, room_id):
        if room_id not in self.rooms:
            # error
            logger.warning(f"Room ID {room_id} not found")
            return None
        return self.rooms[room_id]

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]
            logger.info(f"Room ID {room_id} removed")
        else:
            logger.warning(f"Room ID {room_id} not found")
