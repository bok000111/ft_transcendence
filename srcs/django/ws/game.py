import asyncio
import random
from channels.layers import get_channel_layer
from ws.enums import GameType
from ws.ball import Ball
from ws.player import Player
from ws.ai_player import AI_Player
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


class Game:
    # matched_user = tuple(uid, channel_name, nickname)
    def __init__(self, gid: int, game_type: GameType, matched_users: list):
        self.gid = gid
        self.group_name = f"game_{self.gid}"
        self.game_type = game_type
        if game_type == GameType.AI:
            self.players = [
                (
                    Player(
                        0, matched_users[0][0], matched_users[0][1], matched_users[0][2]
                    )
                ),
                (
                    AI_Player(
                        1, matched_users[0][0], matched_users[0][1], "mingkang_bot"
                    )
                ),
            ]
        elif game_type == GameType.SUB_GAME:
            self.players = [
                Player(idx, uid, channel_name, nickname)
                for idx, (uid, channel_name, nickname) in enumerate(matched_users)
            ]
        else:
            self.players = [
                Player(idx, uid, channel_name, nickname + "_" + str(idx + 1))
                for idx, (uid, channel_name, nickname) in enumerate(matched_users)
            ]
        self.player_count = len(self.players)
        self.ball = Ball()
        self.status = "waiting"
        self.channel_layer = get_channel_layer()
        self.end_score = 5
        # from .tournament import TournamentManager
        # self.tournament_manager = TournamentManager()
        print(self.channel_layer)

    @classmethod
    async def create(cls, id, game_type, matched_users):
        self = cls(id, game_type, matched_users)
        if game_type == GameType.LOCAL or game_type == GameType.AI:
            await self.channel_layer.group_add(
                self.group_name, self.players[0].channel_name
            )
        else:
            await self.add_players_to_group(matched_users)
        return self

    async def start(self, end_score):
        self.status = "playing"
        self.end_score = end_score
        for player in self.players:
            print(f"Player {player.nickname} joined in {self.game_type}")
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "game_info",
                "data_type": "start",
                "uids": [player.uid for player in self.players],
                "message": {
                    "id": self.gid,
                    "type": self.game_type.value,
                    "users": [player.nickname for player in self.players],
                    "end_score": end_score,
                },
            },
        )

        # if self.game_type != GameType.TOURNAMENT:
        asyncio.create_task(self.send_game_info())

    async def add_players_to_group(self, matched_users):
        tasks = [
            self.channel_layer.group_add(self.group_name, channel_name)
            for _, channel_name, _ in matched_users
        ]
        try:
            await asyncio.gather(*tasks)
        except (asyncio.TimeoutError, asyncio.CancelledError) as exc:
            print(f"An error occurred while adding players to group: {exc}")

    async def remove_players_from_group(self):
        tasks = [
            self.channel_layer.group_discard(
                self.group_name, player.channel_name)
            for player in self.players
        ]
        try:
            await asyncio.gather(*tasks)
        except (asyncio.TimeoutError, asyncio.CancelledError) as exc:
            print(
                f"An error occurred while removing players from group: {exc}")

    async def send_game_info(self):
        self.status = "playing"

        if self.game_type == GameType.AI:
            if self.ball.vel["x"] > 0:
                self.players[1].get_destination(self.ball)
                self.players[1].set_state()
        while self.status == "playing":
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "game_info", "data_type": "info", "message": self.info()},
            )
            self.update()
            await asyncio.sleep(1 / 60)
        if self.status == "end":
            # 게임 종료 처리
            # if self.game_type == GameType.TOURNAMENT:
            #     self.tournament_manager.finish_subgame_in_tournament(
            #         self.gid, [self.players[0].score, self.players[1].score])
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "game_info", "data_type": "result",
                    "message": self.result()},
            )

            await self.remove_players_from_group()

    def update(self):
        for player in self.players:
            player.move()
        self.ball.move()
        self.check_collision()
        # check game end(임시)
        if self.player_count == 2:
            if (
                self.players[0].score >= self.end_score
                or self.players[1].score >= self.end_score
            ):
                self.status = "end"
        elif self.player_count == 4:
            if (
                self.players[0].score >= self.end_score
                or self.players[1].score >= self.end_score
                or self.players[2].score >= self.end_score
                or self.players[3].score >= self.end_score
            ):
                self.status = "end"

    # nickname에 해당하는 player의 keyevent를 처리
    def handle_keyevent(self, nickname, keyevent):
        for player in self.players:
            if player.nickname == nickname:
                player.set_state(keyevent)

    def check_collision(self):
        if self.player_count == 2:
            self.check_collision_2p()
        elif self.player_count == 4:
            self.check_collision_4p()

    def update_score(self, winner: Player):
        winner.score += 1
        self.ball.reset_pos(random.randint(1, 2))
        self.players[0].reset_pos()
        self.players[1].reset_pos()
        if self.game_type == GameType.AI and self.ball.vel["x"] > 0:
            self.players[1].get_destination(self.ball)
            self.players[1].set_state()

    def check_collision_2p(self):
        # check wall collision
        if (
            self.ball.pos["y"] <= BALL_RADIUS
            or self.ball.pos["y"] >= SCREEN_HEIGHT - BALL_RADIUS
        ):
            self.ball.pos["y"] = (
                BALL_RADIUS
                if self.ball.pos["y"] <= BALL_RADIUS
                else SCREEN_HEIGHT - BALL_RADIUS
            )
            self.ball.bounce("y")
        # check paddle collision
        if self.ball.pos["x"] <= INTERVAL:
            if (
                self.players[0].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[0].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.pos["x"] = INTERVAL
                self.ball.bounce("x", self.players[0].pos["y"])
                if self.game_type == GameType.AI:
                    self.players[1].get_destination(self.ball)
                    self.players[1].set_state()
            elif self.ball.pos["x"] < 0:
                self.update_score(self.players[1])
        elif self.ball.pos["x"] >= SCREEN_WIDTH - INTERVAL:
            if (
                self.players[1].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[1].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.pos["x"] = SCREEN_WIDTH - INTERVAL
                self.ball.bounce("x", self.players[1].pos["y"])
            elif self.ball.pos["x"] > SCREEN_WIDTH:
                self.update_score(self.players[0])

    def check_collision_4p(self):
        is_loser = [False, False, False, False]
        # check 1p collision
        if self.ball.pos["x"] <= INTERVAL:
            if (
                self.players[0].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[0].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.pos["x"] = INTERVAL
                self.ball.bounce("x", self.players[0].pos["y"])
            elif self.ball.pos["x"] < 0:
                # update score
                is_loser[0] = True
        # check 2p collision
        elif self.ball.pos["x"] >= SCREEN_WIDTH - INTERVAL:
            if (
                self.players[1].pos["y"] - PADDLE_HEIGHT <= self.ball.pos["y"]
                and self.players[1].pos["y"] + PADDLE_HEIGHT >= self.ball.pos["y"]
            ):
                self.ball.pos["x"] = SCREEN_WIDTH - INTERVAL
                self.ball.bounce("x", self.players[1].pos["y"])
            elif self.ball.pos["x"] > SCREEN_WIDTH:
                is_loser[1] = True
        # check 3p collision
        if self.ball.pos["y"] <= INTERVAL:
            if (
                self.players[2].pos["x"] - PADDLE_HEIGHT <= self.ball.pos["x"]
                and self.players[2].pos["x"] + PADDLE_HEIGHT >= self.ball.pos["x"]
            ):
                self.ball.pos["y"] = INTERVAL
                self.ball.bounce("y", self.players[2].pos["x"])
            elif self.ball.pos["y"] < 0:
                is_loser[2] = True
        # check 4p collision
        elif self.ball.pos["y"] >= SCREEN_HEIGHT - INTERVAL:
            if (
                self.players[3].pos["x"] - PADDLE_HEIGHT <= self.ball.pos["x"]
                and self.players[3].pos["x"] + PADDLE_HEIGHT >= self.ball.pos["x"]
            ):
                self.ball.pos["y"] = SCREEN_HEIGHT - INTERVAL
                self.ball.bounce("y", self.players[3].pos["x"])
            elif self.ball.pos["y"] > SCREEN_HEIGHT:
                is_loser[3] = True
        if True in is_loser:
            self.ball.reset_pos(random.randint(1, 4))
            for i in range(4):
                self.players[i].reset_pos()
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
        max_score = max(self.players, key=lambda player: player.score).score
        return {
            "id": self.gid,
            "type": self.game_type.value,
            "users": [player.nickname for player in self.players],
            "winner": [
                player.nickname
                for player in self.players
                if player.score == max([player.score for player in self.players])
            ],
        }

    def get_winner(self):
        # player 2명 일 때 사용
        return (
            self.players[0].uid
            if self.players[0].score > self.players[1].score
            else self.players[1].uid
        )
