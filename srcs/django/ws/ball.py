import math
import random
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


class Ball:
    def __init__(self):
        self.reset_pos(1)
        self.speed_increment = 1.1  # 속도가 증가하는 양
        self.max_speed = MAX_SPEED  # 최대 속도

    def move(self):
        self.pos["x"] += self.vel["x"]
        self.pos["y"] += self.vel["y"]

    def get_bounce_angle(self, intersect):
        normalized_relative_intersect = intersect / PADDLE_HEIGHT
        bounce_angle = normalized_relative_intersect * (math.pi / 4)
        return bounce_angle

    def bounce_paddle(self, paddle_pos, axis):
        if axis == "x":
            bounce_angle = self.get_bounce_angle(self.pos["y"] - paddle_pos)
            self.vel["x"] = round(self.speed * math.cos(bounce_angle), 2)
            if self.pos["x"] > SCREEN_WIDTH / 2:
                self.vel["x"] = -self.vel["x"]
            self.vel["y"] = round(self.speed * math.sin(bounce_angle), 2)
        elif axis == "y":
            bounce_angle = self.get_bounce_angle(self.pos["x"] - paddle_pos)
            self.vel["y"] = round(self.speed * math.cos(bounce_angle), 2)
            if self.pos["y"] > SCREEN_HEIGHT / 2:
                self.vel["y"] = -self.vel["y"]
            self.vel["x"] = round(self.speed * math.sin(bounce_angle), 2)

    def bounce(self, direction, paddle_pos=None):
        if direction == "x":
            if paddle_pos is not None:
                self.bounce_paddle(paddle_pos, "x")
                self.increase_speed()
            else:
                self.vel["x"] = -self.vel["x"]
        elif direction == "y":
            if paddle_pos is not None:
                self.bounce_paddle(paddle_pos, "y")
                self.increase_speed()
            else:
                self.vel["y"] = -self.vel["y"]

    def increase_speed(self):
        # x와 y 방향으로 속도를 증가시킨다. 단, 최대 속도를 초과하지 않도록 한다.
        if self.speed < self.max_speed:
            self.speed *= self.speed_increment

    def reset_pos(self, rand_num):
        self.speed = DEFAULT_SPEED
        self.pos = {"x": SCREEN_WIDTH / 2, "y": SCREEN_HEIGHT / 2}

        # 랜덤한 각도 설정
        if rand_num == 1:
            angle = random.randint(150, 210)
        elif rand_num == 2:
            angle = random.randint(-30, 30)
        elif rand_num == 3:
            angle = random.randint(240, 300)
        elif rand_num == 4:
            angle = random.randint(60, 120)

        # 각도를 라디안으로 변환
        radian = math.radians(angle)

        vel_x = round(self.speed * math.cos(radian), 2)
        vel_y = round(self.speed * math.sin(radian), 2)
        # self.vel = {"x": vel_x, "y": vel_y}
        self.vel = {"x": 8, "y": 6}
