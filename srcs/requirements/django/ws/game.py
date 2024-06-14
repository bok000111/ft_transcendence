from .ball import Ball
from .player import Player
from .constants import *


class Game:
    # 2인용 게임, 4인용 게임 구분
    def __init__(self, id, player_list):
        self.id = id
        self.players = player_list
        self.player_count = len(player_list)
        self.ball = Ball()
        self.status = "waiting"

    def update(self):
        for player in self.players:
            player.move()
        self.ball.move()
        self.check_collision()
        # check game end(임시)
        if self.player_count == 2:
            if self.players[0].score >= 5 or self.players[1].score >= 5:
                self.status = "end"
        elif self.player_count == 4:
            if (
                self.players[0].score >= 5
                or self.players[1].score >= 5
                or self.players[2].score >= 5
                or self.players[3].score >= 5
            ):
                self.status = "end"

    def check_collision(self):
        if self.player_count == 2:
            self.check_collision_2p()
        elif self.player_count == 4:
            self.check_collision_4p()

    def check_collision_2p(self):
        interval = PADDLE_WIDTH * 2 + BALL_RADIUS
        # check wall collision
        if (
            self.ball.pos["y"] <= interval
            or self.ball.pos["y"] >= SCREEN_HEIGHT - interval
        ):
            self.ball.bounce("y")
        # check paddle collision
        if self.ball.pos["x"] <= interval:
            if (
                self.players[0].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[0].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.bounce("x")
            else:
                # update score(함수로 구현할 수도)
                self.players[1].score += 1
                self.ball.reset_pos()
        elif self.ball.pos["x"] >= SCREEN_WIDTH - interval:
            if (
                self.players[1].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[1].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.bounce("x")
            else:
                self.players[0].score += 1
                self.ball.reset_pos()

    def check_collision_4p(self):
        interval = PADDLE_WIDTH * 2 + BALL_RADIUS
        is_loser = [False, False, False, False]
        # check 1p collision
        if self.ball.pos["x"] <= interval:
            if (
                self.players[0].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[0].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.bounce("x")
            else:
                # update score
                is_loser[0] = True
                self.ball.reset_pos()
        # check 2p collision
        elif self.ball.pos["x"] >= SCREEN_WIDTH - interval:
            if (
                self.players[1].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[1].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.bounce("x")
            else:
                is_loser[1] = True
                self.ball.reset_pos()
        # check 3p collision
        if self.ball.pos["y"] <= interval:
            if (
                self.players[2].pos["x"] - PADDLE_HEIGHT <= self.ball.pos["x"]
                and self.players[2].pos["x"] + PADDLE_HEIGHT >= self.ball.pos["x"]
            ):
                self.ball.bounce("y")
            else:
                is_loser[2] = True
                self.ball.reset_pos()
        # check 4p collision
        elif self.ball.pos["y"] >= SCREEN_HEIGHT - interval:
            if (
                self.players[3].pos["x"] - PADDLE_HEIGHT <= self.ball.pos["x"]
                and self.players[3].pos["x"] + PADDLE_HEIGHT >= self.ball.pos["x"]
            ):
                self.ball.bounce("y")
            else:
                is_loser[3] = True
                self.ball.reset_pos()
        if True in is_loser:
            for i in range(4):
                if not is_loser[i]:
                    self.players[i].score += 1

    def info(self):
        return {
            "id": self.id,
            "ball": {"x": self.ball.pos["x"], "y": self.ball.pos["y"]},
            "players": [
                {
                    "nickname": player.nickname,
                    "score": player.score,
                    "x": player.pos["x"],
                    "y": player.pos["y"],
                }
                for player in self.players
            ],
        }

    async def start(self):
        # 대충 게임 시작
        pass

    async def input(self):
        # 대충 입력 받아서 처리
        pass
