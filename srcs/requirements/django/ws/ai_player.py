import threading
import time
import random
from .constants import *
from .player import Player
from .ball import Ball


class AI_Player(Player):
    def __init__(self, idx, uid, channel_name, nickname):
        super().__init__(idx, uid, channel_name, nickname)
        self.destination = SCREEN_HEIGHT / 2

    def get_destination(self, ball):
        if ball.vel["x"] < 0:
            return None
        m = ball.vel["y"] / ball.vel["x"]
        intercept = ball.pos["y"] - m * ball.pos["x"]
        dest = (m * (SCREEN_WIDTH - PADDLE_WIDTH) +
                intercept) % (2 * SCREEN_HEIGHT)
        dest = int(min(dest, 2 * SCREEN_HEIGHT - dest))
        dest = random.randint(
            dest - PADDLE_HEIGHT, dest + PADDLE_HEIGHT)
        if dest < PADDLE_HEIGHT:
            dest = PADDLE_HEIGHT
        elif dest > SCREEN_HEIGHT - PADDLE_HEIGHT:
            dest = SCREEN_HEIGHT - PADDLE_HEIGHT
        self.destination = dest

    def set_state(self):
        if self.pos["y"] > self.destination:
            self.up = True
            self.down = False
        elif self.pos["y"] < self.destination:
            self.up = False
            self.down = True
        else:
            self.up = False
            self.down = False

    def move(self):
        super().move()
        if (self.up and self.pos["y"] <= self.destination) or (self.down and self.pos["y"] >= self.destination):
            self.pos["y"] = self.destination
            self.set_state()
