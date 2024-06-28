import asyncio
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from random import shuffle
from result.deploy import TournamentResultManager
from .roommanager import RoomManager
from .enums import GameType

User = get_user_model()


class TournamentManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self.tournaments = {}  # tournament_id로 Tournament 인스턴스 관리
        self.sub_game_to_tournament = {}  # sub_game의 gid로 tournament 인스턴스 찾아감
        self.tournament_id = 0

    async def create_tournament(self, tournament_users):
        tournament = self.Tournament(
            tournament_users, self.tournament_id, self.sub_game_to_tournament
        )
        self.tournaments[self.tournament_id] = tournament
        self.tournament_id += 1
        print("self.tournament_id: ", self.tournament_id)
        await tournament.init_tournament()

    # gid로 subgame이 끝났음을 알림
    async def finish_subgame_in_tournament(self, gid, scores):
        tid = self.sub_game_to_tournament[gid]
        self.tournaments[tid].finish_subgame(gid, scores)

    class Tournament:
        def __init__(
            self, tournament_users, tournament_id, sub_game_to_tournament
        ) -> None:
            self.tournament_users = tournament_users
            self.tournament_id = tournament_id
            self.sub_game_to_tournament = sub_game_to_tournament
            self.sub_games = {}  # gid로 game_id(1, 2, 3) 관리
            self.winners = []  # semi final winner
            self.tournament_result_manager = None
            self.room_manager = RoomManager()

        async def init_tournament(self):
            # self.tournament_result_manager = await TournamentResultManager.instance()
            # shuffle(self.tournament_users)

            username_list = []
            print("self.tournament_users: ", self.tournament_users)
            for user in self.tournament_users:
                user_info = await sync_to_async(User.objects.get)(pk=user[0])
                username_list.append(user_info.username)
            print("username list for blockchain: ", username_list)
            # self.tournament_result_manager.start_game(
            #     datetime.now().timestamp(), self.tournament_id, username_list
            # )

            tournament_room_id = await self.room_manager.start_game(
                GameType.TOURNAMENT, self.tournament_users
            )
            if tournament_room_id is None:  # error
                return None
            # lock 필요..?
            self.sub_game_to_tournament[tournament_room_id] = self.tournament_id

            await asyncio.sleep(3)
            await asyncio.gather(
                self.start_subgame(self.tournament_users[:2], 2),
                self.start_subgame(self.tournament_users[2:], 3),
            )

        async def start_subgame(self, matched_users, game_id):
            print(matched_users)
            gid = await self.room_manager.start_game(GameType.SUB_GAME, matched_users)
            if gid is None:  # error
                return
            print("subgame gid: ", gid)
            self.sub_games[gid] = game_id

        async def finish_subgame(self, gid, scores):
            # game_info = [gid, self.sub_games[gid], scores[0], scores[1]]
            # self.tournament_result_manager.save_sub_game(
            #     self.tournament_id, game_info)

            if self.sub_games[gid] == 1:
                for x in self.sub_games:
                    self.sub_game_to_tournament.pop(x)
                return None

            if scores[0] > scores[1]:
                winner = self.tournament_users[0 if self.sub_games[gid] == 2 else 2]
            else:
                winner = self.tournament_users[1 if self.sub_games[gid] == 2 else 3]

            self.winners.append(winner)
            if len(self.winners) == 2:
                await self.start_subgame(self.winners, 1)
