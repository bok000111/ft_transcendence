import math
from .constants import *


class Ball:
    def __init__(self):
        self.reset_pos()
        self.speed = DEFAULT_SPEED
        self.speed_increment = 1.1  # 속도가 증가하는 양
        self.max_speed = MAX_SPEED  # 최대 속도
        self.collision_count = 0

    def move(self):
        self.pos["x"] += self.vel["x"]
        self.pos["y"] += self.vel["y"]

    def bounce(self, direction, paddle_pos=None):
        if direction == "x":
            if paddle_pos is not None:
                reflective_intersect_y = self.pos["y"] - paddle_pos
                normalized_relative_intersect_y = reflective_intersect_y / PADDLE_HEIGHT
                bounce_angle = normalized_relative_intersect_y * (math.pi / 4)
                self.vel["x"] = round(self.speed * math.cos(bounce_angle), 2)
                if self.pos["x"] > SCREEN_WIDTH / 2:
                    self.vel["x"] = -self.vel["x"]
                self.vel["y"] = round(self.speed * math.sin(bounce_angle), 2)
            else:
                self.vel["x"] = -self.vel["x"]
        elif direction == "y":
            if paddle_pos is not None:
                reflective_intersect_x = self.pos["x"] - paddle_pos
                normalized_relative_intersect_x = reflective_intersect_x / PADDLE_HEIGHT
                bounce_angle = normalized_relative_intersect_x * (math.pi / 4)
                self.vel["y"] = round(self.speed * math.cos(bounce_angle), 2)
                if self.pos["y"] > SCREEN_HEIGHT / 2:
                    self.vel["y"] = -self.vel["y"]
                self.vel["x"] = -round(self.speed * math.sin(bounce_angle), 2)
            else:
                self.vel["y"] = -self.vel["y"]
        self.collision_count += 1
        if self.collision_count == 1:
            self.increase_speed()
            self.collision_count = 0

    def increase_speed(self):
        # x와 y 방향으로 속도를 증가시킨다. 단, 최대 속도를 초과하지 않도록 한다.
        if self.speed < self.max_speed:
            self.speed *= self.speed_increment

    def reset_pos(self):
        self.pos = {"x": SCREEN_WIDTH / 2, "y": SCREEN_HEIGHT / 2}
        self.vel = {"x": DEFAULT_SPEED_X, "y": DEFAULT_SPEED_Y}
        self.speed = DEFAULT_SPEED
