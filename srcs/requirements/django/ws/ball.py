from .constants import *


class Ball:
    def __init__(self):
        self.reset_pos()
        self.speed_increment = 1  # 속도가 증가하는 양
        self.max_speed = 10  # 볼의 최대 속도

    def move(self):
        self.pos["x"] += self.vel["x"]
        self.pos["y"] += self.vel["y"]

    def bounce(self, direction):
        if direction == "x":
            self.vel["x"] *= -1
        elif direction == "y":
            self.vel["y"] *= -1
        self.increase_speed()

    def increase_speed(self):
        # x와 y 방향으로 속도를 증가시킨다. 단, 최대 속도를 초과하지 않도록 한다.
        if (
            self.vel["x"] > 0
            and self.vel["x"] < self.max_speed
            or self.vel["x"] < 0
            and self.vel["x"] > -self.max_speed
        ):
            self.vel["x"] += (
                self.speed_increment if self.vel["x"] > 0 else -self.speed_increment
            )
        if (
            self.vel["y"] > 0
            and self.vel["y"] < self.max_speed
            or self.vel["y"] < 0
            and self.vel["y"] > -self.max_speed
        ):
            self.vel["y"] += (
                self.speed_increment if self.vel["y"] > 0 else -self.speed_increment
            )

    def reset_pos(self):
        self.pos = {"x": SCREEN_WIDTH / 2, "y": SCREEN_HEIGHT / 2}
        self.vel = {"x": DEFAULT_SPEED, "y": DEFAULT_SPEED}
