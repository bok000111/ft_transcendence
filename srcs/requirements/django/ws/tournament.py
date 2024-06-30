import asyncio
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from random import shuffle
from result.deploy import TournamentResultManager
from datetime import datetime
import os
from .roommanager import RoomManager
from .enums import GameType
import uuid

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
        self.tournament_id = uuid.uuid4().int & (1 << 32) - 1

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
            self.tournament_result_manager = None
            self.channel_layer = channel_layer

        async def update_winner(self, winner):
            print("update_winner: ", winner)
            self.winners.append(winner)
            if len(self.winners) == 2:
                game_event = asyncio.Event()
                game_event.clear()
                gid = await self.room_manager.start_game(
                    GameType.SUB_GAME, self.winners, game_event
                )
                await game_event.wait()
                final_game = self.room_manager.get_game_instance(gid)
                score = final_game.get_scores()
                await self.save_subgame(score, 1)
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
            user_ids = [user[0] for user in self.tournament_users]
            self.tournament_result_manager = await TournamentResultManager.instance()
            print(
                "\033[95m" + f"timestamp: {int(datetime.now().timestamp())}" + "\033[0m"
            )
            await self.tournament_result_manager.start_game(
                self.tournament_id, int(datetime.now().timestamp()), user_ids
            )
            return self

        async def save_subgame(self, score, game_id):
            game_info = [game_id] + score
            print("\033[95m" + f"save subgame: {game_info}" + "\033[0m")
            await self.tournament_result_manager.save_sub_game(
                self.tournament_id, game_info
            )

        async def start_subgame(self, users, game_id):
            print("start_subgame: ", users)
            game_event = asyncio.Event()
            game_event.clear()
            gid = await self.room_manager.start_game(
                GameType.SUB_GAME, users, game_event
            )
            await game_event.wait()
            print("end_subgame gid: ", gid)
            game = self.room_manager.get_game_instance(gid)
            winner_id = game.get_winner()
            score = game.get_scores()
            await self.save_subgame(score, game_id)
            if len(self.winners) < 2:
                for user in self.tournament_users:
                    if user[0] == winner_id:
                        await self.update_winner(user)
                        break

        async def add_players_to_tournament(self, players):
            tasks = [
                self.channel_layer.group_add(self.tournament_name, channel_name)
                for _, channel_name, _ in players
            ]
            try:
                await asyncio.gather(*tasks)
            except Exception as e:
                print(f"An error occurred while adding players to tournament: {e}")

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
