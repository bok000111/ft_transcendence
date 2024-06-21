import asyncio
from channels.layers import get_channel_layer
from ws.enums import GameType
from .ball import Ball
from .player import Player
from .constants import *


class Game:
    # 2인용 게임, 4인용 게임 구분
    # matched_user = tuple(uid, channel_name, nickname)
    def __init__(self, id, game_type, matched_users):
        self.gid = id
        self.group_name = f"game_{self.gid}"
        self.game_type = game_type
        self.players = [
            Player(idx, channel_name, nickname)
            for idx, (_, channel_name, nickname) in enumerate(matched_users)
        ]
        self.player_count = len(self.players)
        self.ball = Ball()
        self.status = "waiting"
        self.channel_layer = get_channel_layer()

    @classmethod
    async def create(cls, id, game_type, matched_users):
        self = cls(id, game_type, matched_users)
        await self.add_players_to_group(matched_users)
        return self

    async def start(self):
        self.status = "playing"
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "game_info",
                "data": "start",
                "message": {
                    "id": self.gid,
                    "type": self.game_type,
                    "users": [player.nickname for player in self.players],
                    "end_score": 5,
                },
            },
        )
        asyncio.create_task(self.send_game_info())

    async def add_players_to_group(self, matched_users):
        tasks = [
            self.channel_layer.group_add(self.group_name, channel_name)
            for _, channel_name, _ in matched_users
        ]
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"An error occurred while adding players to group: {e}")

    async def remove_players_from_group(self):
        tasks = [
            self.channel_layer.group_discard(self.group_name, player.channel_name)
            for player in self.players
        ]
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"An error occurred while removing players from group: {e}")

    async def send_game_info(self):
        while self.status == "playing":
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "game_info", "data": "info", "message": self.info()},
            )
            self.update()
            await asyncio.sleep(1 / 30)
        if self.status == "end":
            # 게임 종료 처리
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "game_info", "data": "result", "message": self.result()},
            )
            await self.remove_players_from_group()

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

    # nickname에 해당하는 player의 keyevent를 처리
    def input(self, nickname, keyevent):
        for player in self.players:
            if player.nickname == nickname:
                player.set_state(keyevent)

    def check_collision(self):
        if self.player_count == 2:
            self.check_collision_2p()
        elif self.player_count == 4:
            self.check_collision_4p()

    def check_collision_2p(self):
        INTERVAL = PADDLE_WIDTH * 2 + BALL_RADIUS
        # check wall collision
        if (
            self.ball.pos["y"] <= INTERVAL
            or self.ball.pos["y"] >= SCREEN_HEIGHT - INTERVAL
        ):
            self.ball.bounce("y")
        # check paddle collision
        if self.ball.pos["x"] <= INTERVAL:
            if (
                self.players[0].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[0].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.bounce("x")
            else:
                # update score(함수로 구현할 수도)
                self.players[1].score += 1
                self.ball.reset_pos()
        elif self.ball.pos["x"] >= SCREEN_WIDTH - INTERVAL:
            if (
                self.players[1].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[1].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.bounce("x")
            else:
                self.players[0].score += 1
                self.ball.reset_pos()

    def check_collision_4p(self):
        INTERVAL = PADDLE_WIDTH * 2 + BALL_RADIUS
        is_loser = [False, False, False, False]
        # check 1p collision
        if self.ball.pos["x"] <= INTERVAL:
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
        elif self.ball.pos["x"] >= SCREEN_WIDTH - INTERVAL:
            if (
                self.players[1].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[1].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.bounce("x")
            else:
                is_loser[1] = True
                self.ball.reset_pos()
        # check 3p collision
        if self.ball.pos["y"] <= INTERVAL:
            if (
                self.players[2].pos["x"] - PADDLE_HEIGHT <= self.ball.pos["x"]
                and self.players[2].pos["x"] + PADDLE_HEIGHT >= self.ball.pos["x"]
            ):
                self.ball.bounce("y")
            else:
                is_loser[2] = True
                self.ball.reset_pos()
        # check 4p collision
        elif self.ball.pos["y"] >= SCREEN_HEIGHT - INTERVAL:
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
            "id": self.gid,
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

    def result(self):
        return {
            "id": self.gid,
            "type": self.game_type,
            "users": [player.nickname for player in self.players],
            "winner": max(self.players, key=lambda x: x.score),
        }

    async def input(self):
        # 대충 입력 받아서 처리
        pass
