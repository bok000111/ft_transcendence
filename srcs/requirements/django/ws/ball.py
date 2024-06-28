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
        self.reset_pos()
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
        self.speed = DEFAULT_SPEED
        self.pos = {"x": SCREEN_WIDTH / 2, "y": SCREEN_HEIGHT / 2}
        min_angle = 15
        max_angle = 75

        # 랜덤한 각도 설정 (10도에서 80도 사이 또는 100도에서 170도 사이)
        random_int = random.randint(0, 3)
        if random_int == 0:
            angle = random.uniform(min_angle, max_angle)
        elif random_int == 1:
            angle = random.uniform(180 - max_angle, 180 - min_angle)
        elif random_int == 2:
            angle = random.uniform(180 + min_angle, 180 + max_angle)
        elif random_int == 3:
            angle = random.uniform(360 - max_angle, 360 - min_angle)

        # 각도를 라디안으로 변환
        radian = math.radians(angle)
        # print angle from radian to degree

        vel_x = round(self.speed * math.cos(radian), 2)
        vel_y = round(self.speed * math.sin(radian), 2)
        self.vel = {"x": vel_x, "y": vel_y}
        # self.vel = {"x": 10, "y": 0}
