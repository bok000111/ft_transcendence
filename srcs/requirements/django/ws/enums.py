from enum import Enum


class WebSocketActionType(Enum):
    JOIN = "join"
    LEAVE = "leave"
    GAME_INPUT = "game_input"
    ME = "me"
    ERROR = "error"
    WAIT = "wait"
    START = "start"
    GAME = "game"
    END = "end"
    NONE = None


class GameType(Enum):
    NORMAL_2 = 0
    NORMAL_4 = 1
    TOURNAMENT = 2
    LOCAL = 3

    @classmethod
    def max_player(cls, game_type: "GameType") -> int:
        if game_type == cls.NORMAL_2:
            return 2
        if game_type == cls.NORMAL_4:
            return 4
        if game_type == cls.TOURNAMENT:
            return 4
        if game_type == cls.LOCAL:
            return 2
        return None
