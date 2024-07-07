from ws.constants import (
    BALL_RADIUS,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DEFAULT_SPEED,
    MAX_SPEED,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    INTERVAL,
)


class Player:
    def __init__(self, idx: int, uid: int, channel_name: str, nickname: str):
        self.idx = idx
        self.uid = uid
        self.channel_name = channel_name
        self.nickname = nickname
        self.reset_pos()
        self.score = 0

    def initial_position(self):
        if self.idx == 0:
            return {"x": PADDLE_WIDTH, "y": SCREEN_HEIGHT / 2}
        if self.idx == 1:
            return {"x": SCREEN_WIDTH - PADDLE_WIDTH, "y": SCREEN_HEIGHT / 2}
        if self.idx == 2:
            return {"x": SCREEN_WIDTH / 2, "y": PADDLE_WIDTH}
        if self.idx == 3:
            return {"x": SCREEN_WIDTH / 2, "y": SCREEN_HEIGHT - PADDLE_WIDTH}

        raise ValueError("Invalid player index")

    # keyevent -> {
    # 1 : x방향 + 키가 눌림.
    # 2 : x방향 - 키가 눌림.
    # 3 : x방향 + 키 떼짐.
    # 4 : x방향 - 키 떼짐.
    # 5 : y방향 + 키가 눌림.
    # 6 : y방향 - 키가 눌림.
    # 7 : y방향 + 키 떼짐.
    # 8 : y방향 - 키 떼짐.
    # }
    def set_state(self, keyevent):
        if keyevent in (1, 6):
            self.up = True
        elif keyevent in (2, 5):
            self.down = True
        elif keyevent in (3, 8):
            self.up = False
        elif keyevent in (4, 7):
            self.down = False

    def move(self):
        if self.idx <= 1:
            if self.up and self.pos["y"] > PADDLE_HEIGHT:
                self.pos["y"] = max(
                    self.pos["y"] - PADDLE_SPEED, PADDLE_HEIGHT)
            elif self.down and self.pos["y"] < SCREEN_HEIGHT - PADDLE_HEIGHT:
                self.pos["y"] = min(
                    self.pos["y"] + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT
                )
        else:
            if self.down and self.pos["x"] > PADDLE_HEIGHT:
                self.pos["x"] = max(
                    self.pos["x"] - PADDLE_SPEED, PADDLE_HEIGHT)
            elif self.up and self.pos["x"] < SCREEN_WIDTH - PADDLE_HEIGHT:
                self.pos["x"] = min(
                    self.pos["x"] + PADDLE_SPEED, SCREEN_WIDTH - PADDLE_HEIGHT
                )

    def reset_pos(self):
        self.pos = self.initial_position()
        self.up = False
        self.down = False

    def reset_score(self):
        self.score = 0
