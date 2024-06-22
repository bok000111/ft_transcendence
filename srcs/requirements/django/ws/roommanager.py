import logging
import uuid
from .game import Game

logger = logging.getLogger(__name__)


# Game class의 싱글톤 패턴 적용
class RoomManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RoomManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.rooms = {}
        return cls._instance

    async def create_game(self, game_type, matched_users):
        try:
            room_id = uuid.uuid4().int
            if room_id in self.rooms:
                logger.warning(f"Room ID {room_id} already exists")
                return None
            # matched_user = (uid, channel_name, nickname)
            self.rooms[room_id] = await Game.create(room_id, game_type, matched_users)
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
