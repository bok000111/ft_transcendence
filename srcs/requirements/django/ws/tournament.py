import asyncio
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from random import shuffle
from .result import TournamentResultManager
from dotenv import load_dotenv

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
        self.sub_games = {}
        self.tournament_id = 0
    
    async def create_tournament(self, user_ids):
        tournament = self.Tournament(user_ids, self.tournament_id, self.sub_games)
        tournament.start_tournament()
        self.tournament_id += 1
        
    async def get_subgame_result(self, gid, result):
    
    class Tournament:
        class TournamenetUser:
            def __init__(self, user_id) -> None:
                self.user_id = user_id
                user_info = User.objects.get(pk=user_id)
                self.username = user_info.username
                self.nickname = user_info.nickname
                self.tournament_id = tournament_id
        
        def __init__(self, user_ids, tournament_id, sub_games) -> None:
            self.game_type = GameType.TOURNAMENT
            self.users = shuffle([self.TournamenetUser(user_id) for user_id in user_ids])
            self.tournament_id = tournament_id
            self.sub_games = sub_games
            # self.channel_layer = get_channel_layer()
            # self.channel_name = "tournament"
            self.tournamentResultmanager = TournamentResultManager(os.getenv("ENDPOINT"))
            self.gids = []

        async def start_tournament(self):
            self.start_subgame([uid for uid in self.users[:2]])
            self.start_subgame([uid for uid in self.users[2:4]])
            
            game.start(1,2)
            game.start(3,4)
            # while semi1.done() and semi2.done():
                
            await semi1
            await semi2
            
            asyncio.sleep(5)
            await self.start_subgame([semi1.result(), semi2.result()])
            

        async def get_winner(self):
            pass

        async def start_subgame(self, matched_uids):
            room_manager = RoomManager()
            gid = await room_manager.create_game(self.game_type, matched_uids)
            if gid is None:
                print("Failed to create game")
                return None
            game = room_manager.get_game_instance(gid)
            if game is None:
                print("Failed to get game instance")
                return None
            # group_name = f"game_{gid}"
            # self.channel_layer.group_add(group_name, self.channel_name)
            self.sub_games[gid] = self.tournament_id
            gids.append(gid)
            await game.start()
            
            # asyncio.create_task(get_winner(group_name))
            

        async def finish_match(self, winner):
            # 대충 내부 경기 끝났을 때 처리 이긴사람 받아서 처리
            pass
