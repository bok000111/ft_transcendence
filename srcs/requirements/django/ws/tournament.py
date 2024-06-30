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
        self.tournament_id = 0

    async def create_tournament(self, tournament_users, channel_layer):
        tournament = await self.Tournament.create(
            tournament_users,
            self.tournament_id,
            channel_layer,
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
        def __init__(self, tournament_users, tournament_id, channel_layer) -> None:
            self.room_manager = RoomManager()
            self.tournament_users = []
            for idx, (uid, channel_name, nickname) in enumerate(tournament_users):
                self.tournament_users.append(
                    (uid, channel_name, nickname + f"_{idx + 1}")
                )
            # tournament_users의 뒤에 idx를 붙여서 4명으로 만들어주기
            self.tournament_id = tournament_id
            self.tournament_name = f"tournament_{tournament_id}"
            self.winners = []
            self.games = []
            # self.tournament_result_manager = TournamentResultManager(
            #     os.getenv("ENDPOINT")
            # )
            self.channel_layer = channel_layer

        async def update_winner(self, winner):
            print("update_winner: ", winner)
            self.winners.append(winner)
            if len(self.winners) == 2:
                game_event = asyncio.Event()
                game_event.clear()
                gid = await self.room_manager.start_game(GameType.SUB_GAME, self.winners, game_event)
                await game_event.wait()
                final_game = self.room_manager.get_game_instance(gid)
                await self.channel_layer.group_send(
                    self.tournament_name,
                    {"type": "game_info", "data_type": "result", "message": final_game.result()})
                await asyncio.sleep(3)
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

        @classmethod
        async def create(cls, tournament_users, tournament_id, channel_layer):
            # shuffle(tournament_users)
            self = cls(tournament_users, tournament_id, channel_layer)
            for user in tournament_users:
                print(f"tournament_users: {user[2]}")
            await self.add_players_to_tournament(tournament_users)
            return self

        async def start_subgame(self, users):
            print("start_subgame: ", users)
            game_event = asyncio.Event()
            game_event.clear()
            # 나중에 event 넣는 부분 리팩토링 하기
            gid = await self.room_manager.start_game(GameType.SUB_GAME, users, game_event)
            await game_event.wait()
            game = self.room_manager.get_game_instance(gid)
            await self.channel_layer.group_send(
                self.tournament_name,
                {"type": "game_info", "data_type": "result", "message": game.result()})
            print("end_subgame gid: ", gid)
            winner_id = game.get_winner()
            if len(self.winners) < 2:
                for user in self.tournament_users:
                    if user[0] == winner_id:
                        await self.update_winner(user)
                        break

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

        def tournament_info(self):
            return {
                "id": self.tournament_id,
                "type": GameType.TOURNAMENT.value,
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
