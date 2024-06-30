import asyncio
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from random import shuffle
from result.deploy import TournamentResultManager
from datetime import datetime
import os
from .roommanager import RoomManager
from .enums import GameType

from channels.layers import get_channel_layer

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
        tournament = await self.Tournament.create(
            tournament_users, self.tournament_id, self.sub_game_to_tournament
        )
        # await tournament.init_tournament()
        self.tournaments[self.tournament_id] = tournament
        self.tournament_id += 1
        print("self.tournament_id: ", self.tournament_id)
        return tournament

    def get_tournament(self, tid):
        if tid in self.tournaments:
            return self.tournaments[tid]
        print(f"Warning: Tournament ID {tid} not found")
        return None

    # gid로 subgame이 끝났음을 알림
    # async def finish_subgame_in_tournament(self, gid, scores):
    #     tid = self.sub_game_to_tournament[gid]
    #     self.tournaments[tid].finish_subgame(gid, scores)

    class Tournament:
        def __init__(
            self, tournament_users, tournament_id, sub_game_to_tournament
        ) -> None:
            self.room_manager = RoomManager()
            self.tournament_users = []
            for idx, (uid, channel_name, nickname) in enumerate(tournament_users):
                self.tournament_users.append(
                    (uid, channel_name, nickname + f"_{idx + 1}")
                )
            # tournament_users의 뒤에 idx를 붙여서 4명으로 만들어주기
            self.tournament_id = tournament_id
            self.tournament_name = f"tournament_{tournament_id}"
            self.games = []
            self.channel_layer = get_channel_layer()
            self.tournament_result_manager = None

        @classmethod
        async def create(cls, tournament_users, tournament_id, sub_game_to_tournament):
            # shuffle(tournament_users)
            self = cls(tournament_users, tournament_id, sub_game_to_tournament)
            await self.add_players_to_tournament(tournament_users)
            return self

        async def start_subgame(self, matched_users, game_id):
            gid = await self.room_manager.start_game(GameType.SUB_GAME, matched_users)
            self.games.append((gid, game_id))

        async def save_subgame(self, gid, game_id):
            game_instance = await self.room_manager.get_game_instance(gid)
            scores = game_instance.get_scores()
            game_info = [game_id] + scores
            self.tournament_result_manager.save_sub_game(
                self.tournament_id, game_info)
            # async def wait_for_game_end(self, game_id):
            #     while self.room_manager.check_status(game_id) != "end":
            #         await asyncio.sleep(1)

        async def start_tournament(self):
            # self.tournament_result_manager = await TournamentResultManager.instance()
            # user_ids = [user[0] for user in self.tournament_users]
            # self.tournament_result_manager.start_game(
            #     datetime.now().timestamp(), self.tournament_id, user_ids
            # )
            await self.channel_layer.group_send(
                self.tournament_name,
                {
                    "type": "tournament_info",
                    "uids": [user[0] for user in self.tournament_users],
                    "message": self.tournament_info(),
                },
            )

            # await asyncio.sleep(2)
            await asyncio.gather(
                self.start_subgame(self.tournament_users[:2], 2),
                self.start_subgame(self.tournament_users[2:], 3),
            )
            # game1 = asyncio.create_task(
            #     self.room_manager.start_game(
            #         GameType.SUB_GAME, self.tournament_users[:2]
            #     )
            # )
            # game2 = asyncio.create_task(
            #     self.room_manager.start_game(
            #         GameType.SUB_GAME, self.tournament_users[2:]
            #     )
            # )
            # self.games.append(await game1)
            # self.games.append(await game2)
            # send group message(end)
            # game1_instance = self.room_manager.get_game_instance(self.games[0])
            # game2_instance = self.room_manager.get_game_instance(self.games[1])

            # games 둘 다 끝날 때까지 대기(game 나중에 끝나면 제거해주기)
            while (
                self.room_manager.check_status(self.games[0]) != "end"
                or self.room_manager.check_status(self.games[1]) != "end"
            ):
                print(
                    "\033[95m" + "game1: ",
                    self.room_manager.check_status(self.games[0]) + "\033[0m",
                )
                print(
                    "\033[95m" + "game2: ",
                    self.room_manager.check_status(self.games[1]) + "\033[0m",
                )
                await asyncio.sleep(1)

            # for game in self.games:
            #     await self.save_subgame(game[0], game[1])

            final_users = []
            if (
                self.tournament_users[0][0]
                == self.room_manager.get_game_instance(self.games[0]).get_winner()
            ):
                final_users.append(self.tournament_users[0])
                print(f"winner1: {self.tournament_users[0][2]}")
            else:
                final_users.append(self.tournament_users[1])
                print(f"winner1: {self.tournament_users[1][2]}")
            if (
                self.tournament_users[2][0]
                == self.room_manager.get_game_instance(self.games[1]).get_winner()
            ):
                final_users.append(self.tournament_users[2])
                print(f"winner2: {self.tournament_users[2][2]}")
            else:
                final_users.append(self.tournament_users[3])
                print(f"winner2: {self.tournament_users[3][2]}")
            print(f"final_users: {final_users[0][2]}, {final_users[1][2]}")
            self.games.append(
                await self.room_manager.start_game(GameType.SUB_GAME, final_users)
            )
            while self.room_manager.check_status(self.games[2]) != "end":
                await asyncio.sleep(1)
            final_game = self.room_manager.get_game_instance(self.games[2])

            await self.channel_layer.group_send(
                self.tournament_name,
                {
                    "type": "tournament_result",
                    "message": {
                        "id": self.tournament_id,
                        "type": GameType.TOURNAMENT.value,
                        "users": self.tournament_users,
                        "winner": final_game.result()["winner"],
                    },
                },
            )
            # await self.save_subgame(final_game.gid, 1)
            # remove games
            # for game in self.games:
            #     self.room_manager.remove_room(game)

        async def add_players_to_tournament(self, players):
            tasks = [
                self.channel_layer.group_add(
                    self.tournament_name, channel_name)
                for _, channel_name, _ in players
            ]
            try:
                await asyncio.gather(*tasks)
            except Exception as e:
                print(
                    f"An error occurred while adding players to tournament: {e}")

        async def init_tournament(self):
            # shuffle(self.tournament_users)

            username_list = []
            print("self.tournament_users: ", self.tournament_users)
            for user in self.tournament_users:
                user_info = await sync_to_async(User.objects.get)(pk=user[0])
                username_list.append(user_info.username)
            print(username_list)
            # self.tournament_result_manager.start_game(
            #     datetime.now().timestamp(), self.tournament_id, username_list
            # )

            room_manager = RoomManager()
            tournament_room_id = await room_manager.start_game(
                GameType.TOURNAMENT, self.tournament_users
            )
            if tournament_room_id is None:  # error
                return None
            # lock 필요..?
            self.sub_game_to_tournament[tournament_room_id] = self.tournament_id

            await asyncio.gather(
                self.start_subgame(self.tournament_users[:2], 2),
                self.start_subgame(self.tournament_users[2:], 3),
            )

        # async def start_subgame(self, matched_users, game_id):
        #     room_manager = RoomManager()
        #     gid = await room_manager.start_game(GameType.SUB_GAME, matched_users)
        #     if gid is None:  # error
        #         return
        #     self.sub_games[gid] = game_id

        # async def finish_subgame(self, gid, scores):
        #     # game_info = [gid, self.sub_games[gid], scores[0], scores[1]]
        #     # self.tournament_result_manager.save_sub_game(
        #     #     self.tournament_id, game_info)

        #     if self.sub_games[gid] == 1:
        #         for x in self.sub_games:
        #             self.sub_game_to_tournament.pop(x)
        #         return None

        #     if scores[0] > scores[1]:
        #         winner = self.tournament_users[0 if self.sub_games[gid] == 2 else 2]
        #     else:
        #         winner = self.tournament_users[1 if self.sub_games[gid] == 2 else 3]

        #     self.winners.append(winner)
        #     if len(self.winners) == 2:
        #         self.start_subgame(self.winners, 1)

        # message: {
        #     "code": number,
        #     "action": "start",
        #     "data": {
        #         "id": number,
        #         "type": TOURNAMENT (= 2),
        #         "users": [ player1, player2, player3, player4 ],
        #         "end_score": number,
        #         "my_nickname": str
        #     },
        # }
        def tournament_info(self):
            return {
                "id": self.tournament_id,
                "type": GameType.TOURNAMENT.value,
                # [nickname1, nickname2, nickname3, nickname4]
                "users": [user[2] for user in self.tournament_users],
                "end_score": 7,
            }

        def tournament_result(self):
            return {
                "id": self.tournament_id,
                "type": GameType.TOURNAMENT.value,
                "users": [user[2] for user in self.tournament_users],
                "winner": [self.final_winner],
            }
