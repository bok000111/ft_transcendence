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
