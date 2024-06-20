from enum import Enum


class WebSocketActionType(Enum):
    JOIN = "join", "join.queue"
    LEAVE = "leave", "leave.queue"
    GAME_INPUT = "game_input", "game.input"
    ME = "me", "me.info"
    ERROR = "error", "error"
    WAIT = "wait", "wait.queue"
    START = "start", "game.start"
    GAME = "game", "game.info"
    END = "end", "game.end"

    @property
    def type(self) -> str:
        return self.value[1]

    @classmethod
    def from_str(cls, value: str):
        for action in WebSocketActionType:
            if action.value[0] == value:
                return action
        return None


class GameType(Enum):
    NORMAL_2 = 0
    NORMAL_4 = 1
    TOURNAMENT = 2
    LOCAL = 3
    AI = 4

    def max_player(self) -> int:
        if self is self.NORMAL_2 or self is self.LOCAL:
            return 2
        if self is self.NORMAL_4 or self is self.TOURNAMENT:
            return 4
        if self is self.AI:
            return 1
        return None

    def max_client(self) -> int:
        if self is self.NORMAL_2:
            return 2
        if self is self.NORMAL_4 or self is self.TOURNAMENT:
            return 4
        if self is self.LOCAL or self is self.AI:
            return 1
        return None
