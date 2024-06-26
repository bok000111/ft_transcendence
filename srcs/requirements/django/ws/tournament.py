import asyncio
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from random import shuffle
from ..result import TournamentResultManager
from dotenv import load_dotenv
from datetime import datetime
import os
from roommanager import RoomManager
from enums import GameType

User = get_user_model()


class TournamentManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self.tournaments = {}  # tournament_id로 Tournament 인스턴스 관리
        self.sub_game_to_tournament = {}  # sub_game의 gid로 tournament 인스턴스 찾아감
        self.tournament_id = 0

    async def create_tournament(self, user_ids):
        tournament = self.Tournament(user_ids, self.tournament_id)
        tournament.init_tournament()
        self.tournaments[self.tournament_id] = tournament
        self.tournament_id += 1

    # gid로 subgame이 끝났음을 알림
    async def finish_subgame_in_tournament(self, gid, scores):
        tid = self.sub_game_to_tournament[gid]
        self.tournaments[tid].finish_subgame(gid, scores)

    class Tournament:
        class TournamenetUser:
            def __init__(self, user_id) -> None:
                self.user_id = user_id
                user_info = User.objects.get(pk=user_id)
                self.username = user_info.username
                self.nickname = user_info.nickname

        def __init__(self, user_ids, tournament_id, sub_game_to_tournament) -> None:
            self.users = shuffle(
                [self.TournamenetUser(user_id) for user_id in user_ids]
            )
            self.tournament_id = tournament_id
            self.tournament_result_manager = TournamentResultManager(
                os.getenv("ENDPOINT")
            )
            self.sub_games = {}  # gid로 game_id(1, 2, 3) 관리
            self.sub_game_to_tournament = sub_game_to_tournament
            self.winners = []  # 승자 관리(TournamentUser)

        async def init_tournament(self):
            self.tournament_result_manager.start_game(
                datetime.now().timestamp(), self.tournament_id, self.users
            )
            self.start_subgame([uid for uid in self.users[:2]])
            self.start_subgame([uid for uid in self.users[2:4]])

        async def start_subgame(self, matched_uids, game_id):
            room_manager = RoomManager()
            gid = await room_manager.start_game(GameType.TOURNAMENT, matched_uids)
            self.sub_game_to_tournament[gid] = self.tournament_id  # lock 필요..?
            self.sub_games[gid] = game_id

        async def finish_subgame(self, gid, scores: int[2]):
            game_info = [gid, self.sub_games[gid], scores[0], scores[1]]
            self.tournament_result_manager.save_sub_game(self.tournament_id, game_info)
            if scores[0] > scores[1]:
                winner = self.users[0 if self.sub_games[gid] == 2 else 2]
            else:
                winner = self.users[1 if self.sub_games[gid] == 2 else 3]

            self.winners.append(winner)
            if len(winner) == 2:
                self.users = self.winners
                self.start_subgame(winner, 1)

            elif self.sub_games[gid] == 1:
                for x in self.sub_games:
                    self.sub_game_to_tournament.pop(x)
