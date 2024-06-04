import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer


User = get_user_model()


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(code=401, reason="auth required")

        self.user = self.scope["user"]
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]

        match action:
            case "":
                pass

    #


class Lobby:
    async def start(self):
        # 대충 게임 만들어서 시작하고 게임 객체 반환
        pass

    async def set_nick(self, user, nick: str):
        # 대충 닉네임 설정
        pass

    async def ready(self, user):
        # 대충 유저가 준비했다고 처리
        pass

    async def config(self, user, config):
        # 대충 유저가 설정을 보냈을 때 처리
        pass


class Game:
    def __init__(self) -> None:
        # 대충 게임 초기화
        pass

    async def start(self):
        # 대충 게임 시작
        pass

    async def input(self):
        # 대충 입력 받아서 처리
        pass


class Tournament:
    def __init__(self) -> None:
        # 매칭된 유저들 받아서 토너먼트 시작
        pass

    async def start(self):
        # 대충 토너먼트 시작 하위 2개의 게임 객체 생성하고 시작
        pass

    async def finish_match(self, winner):
        # 대충 내부 경기 끝났을 때 처리 이긴사람 받아서 처리
        pass
