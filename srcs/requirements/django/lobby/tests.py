import json
import faker

from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async, async_to_sync

# from channels.auth import AuthMiddlewareStack
# from channels.testing import WebsocketCommunicator
# from channels.routing import URLRouter

# from ft_transcendence.tests import login, logout, channels_reverse
# from ft_transcendence.routing import urlpatterns

from lobby.models import GameLobby
from user.tests import UserFactory
from lobby.factories import LobbyPostFactory

User = get_user_model()

signup_url = reverse("signup")
login_url = reverse("login")
logout_url = reverse("logout")
lobby_url = reverse("lobby")


class LobbyTest(TransactionTestCase):
    def setUp(self):
        self.host = {
            "user": UserFactory(),
            "client": Client(),
        }
        self.host["client"].force_login(self.host["user"])
        self.user = UserFactory()
        self.client = Client()
        self.client.force_login(self.user)

        self.user2 = UserFactory()
        self.client2 = Client()
        self.client2.force_login(self.user2)

    def test_create_lobby(self):
        response = self.client.post(
            lobby_url,
            LobbyPostFactory(),
            content_type="application/json",
        )

        self.assertContains(response, "Lobby created", status_code=201)

    def test_create_lobby_invalid_format(self):
        tcs = [
            LobbyPostFactory(name=""),
            LobbyPostFactory(max_players=20),
            LobbyPostFactory(end_score=50),
        ]

        responses = [
            self.client.post(
                lobby_url,
                tc,
                content_type="application/json",
            )
            for tc in tcs
        ]

        self.assertContains(responses[0], "required", status_code=400)
        self.assertContains(responses[1], "invalid", status_code=400)
        self.assertContains(responses[2], "invalid", status_code=400)

    def test_get_lobby_list(self):
        tcs = [LobbyPostFactory() for _ in range(5)]

        for tc in tcs:
            self.host["client"].post(
                lobby_url,
                tc,
                content_type="application/json",
            )

        response = self.client.get(lobby_url)

        self.assertContains(response, "Lobbies", status_code=200)
        self.assertEqual(len(response.json()["data"]["lobbies"]), 5)
        for tc in tcs:
            self.assertContains(response, tc["name"], status_code=200)

    def test_get_lobby_detail(self):
        tcs = [LobbyPostFactory() for _ in range(5)]

        for tc in tcs:
            response = self.host["client"].post(
                lobby_url,
                tc,
                content_type="application/json",
            )
            lobby_id = response.json()["data"]["lobby"]["id"]
            response = self.client.get(reverse("lobby_detail", args=[lobby_id]))
            self.assertContains(response, "Lobby", status_code=200)

    def test_join_leave_lobby(self):
        response = self.host["client"].post(
            lobby_url,
            LobbyPostFactory(),
            content_type="application/json",
        )

        lobby_id = response.json()["data"]["lobby"]["id"]

        response = self.client.post(
            reverse("lobby_detail", args=[lobby_id]),
            content_type="application/json",
            data={"nickname": "testnick"},
        )

        self.assertContains(response, "Joined lobby", status_code=200)

        response = self.client.get(
            reverse("lobby_detail", args=[lobby_id]),
            content_type="application/json",
        )

        self.assertContains(response, self.user.username, status_code=200)

        response = self.client.delete(
            reverse("lobby_detail", args=[lobby_id]),
        )

        self.assertContains(response, "Left lobby", status_code=200)

        response = self.client.get(
            reverse("lobby_detail", args=[lobby_id]),
            content_type="application/json",
        )

        self.assertNotContains(response, self.user.username, status_code=200)

        response = self.host["client"].delete(
            reverse("lobby_detail", args=[lobby_id]),
        )

        self.assertContains(response, "Lobby deleted", status_code=200)

        response = self.host["client"].get(
            reverse("lobby_detail", args=[lobby_id]),
            content_type="application/json",
        )

        self.assertContains(response, "Not found", status_code=404)

    def test_dup_nickname(self):
        response = self.host["client"].post(
            lobby_url,
            LobbyPostFactory(),
            content_type="application/json",
        )
        lobby_id = response.json()["data"]["lobby"]["id"]

        response = self.client.post(
            reverse("lobby_detail", args=[lobby_id]),
            content_type="application/json",
            data={"nickname": "duptest"},
        )
        self.assertContains(response, "Joined lobby", status_code=200)

        response = self.client2.post(
            reverse("lobby_detail", args=[lobby_id]),
            content_type="application/json",
            data={"nickname": "duptest"},
        )
        self.assertContains(response, "Nickname is already in use", status_code=400)

    def test_same_lobby(self):
        response = self.host["client"].post(
            lobby_url,
            LobbyPostFactory(),
            content_type="application/json",
        )
        lobby_id = response.json()["data"]["lobby"]["id"]

        response = self.client.post(
            reverse("lobby_detail", args=[lobby_id]),
            content_type="application/json",
            data={"nickname": "testnick2"},
        )
        self.assertContains(response, "Joined lobby", status_code=200)

        response = self.client.post(
            reverse("lobby_detail", args=[lobby_id]),
            content_type="application/json",
            data={"nickname": "testnick3"},
        )

        self.assertContains(response, "Already in the lobby", status_code=400)

    def test_user_already_in_another_lobby(self):
        response = self.host["client"].post(
            lobby_url,
            LobbyPostFactory(),
            content_type="application/json",
        )
        lobby_id1 = response.json()["data"]["lobby"]["id"]

        response = self.host["client"].post(
            lobby_url,
            LobbyPostFactory(),
            content_type="application/json",
        )
        lobby_id2 = response.json()["data"]["lobby"]["id"]

        response = self.client.post(
            reverse("lobby_detail", args=[lobby_id1]),
            content_type="application/json",
            data={"nickname": "testnick2"},
        )
        self.assertContains(response, "Joined lobby", status_code=200)

        response = self.client.post(
            reverse("lobby_detail", args=[lobby_id2]),
            content_type="application/json",
            data={"nickname": "testnick3"},
        )

        print(response.json())
        self.assertContains(
            response, "The user is already in some lobby", status_code=400
        )


# class RoomWebSocketTest(TransactionTestCase):
#     async def asyncSetUp(self):
#         self.cookies = await login(**TEST_LOGIN_DATA)

#     def setUp(self):
#         self.async_client = AsyncClient()

#         async_to_sync(self.async_client.post)(
#             signup_url,
#             json.dumps(TEST_USER_DATA),
#             content_type="application/json",
#         )

#         async_to_sync(self.async_client.post)(
#             login_url,
#             json.dumps(TEST_LOGIN_DATA),
#             content_type="application/json",
#         )

#         response = async_to_sync(self.async_client.post)(
#         )
#             create_room_url,
#             json.dumps(TEST_ROOM_DATA),
#             content_type="application/json",
#         self.room_id = response.json().get("room_id", None)

#         asyncio.run(self.asyncSetUp())

#     async def asyncTearDown(self):
#         pass

#     def tearDown(self):
#         asyncio.run(self.asyncTearDown())

#     async def test_ws_unauth(self):
#         self.communicator = WebsocketCommunicator(
#             AuthMiddlewareStack(URLRouter(urlpatterns)),
#             f"/ws/pong/{self.room_id}/",
#         )

#         connected, code = await self.communicator.connect()

#         self.assertFalse(connected)
#         self.assertEqual(code, 403)

#     async def test_ws_connect(self):
#         self.communicator = WebsocketCommunicator(
#             AuthMiddlewareStack(URLRouter(urlpatterns)),
#             f"/ws/pong/{self.room_id}/",
#             headers=[(b"cookie", self.cookies.output(header="", sep=";").encode())],
#         )

#         connected, subprotocol = await self.communicator.connect()

#         self.assertTrue(connected)

#         recv = await self.communicator.receive_json_from()
#         assert recv["message"] == f"Connected to room {self.room_id}"

#         await self.communicator.disconnect()


# # class RoomWSTest(TransactionTestCase):
# #     def setUp(self):
# #         self.async_client = AsyncClient()

# #         async_to_sync(self.async_client.post)(
# #             signup_url,
# #             json.dumps(TEST_USER_DATA),
# #             content_type="application/json",
# #         )

# #         response = async_to_sync(self.async_client.post)(
# #             login_url,
# #             json.dumps(TEST_LOGIN_DATA),
# #             content_type="application/json",
# #         )
# #         self.cookies = response.cookies

# #         response = async_to_sync(self.async_client.post)(
# #             create_room_url,
# #             json.dumps(TEST_ROOM_DATA),
# #             content_type="application/json",
# #         )

# #         self.room_id = response.json().get("room_id", None)

# #     async def test_ws_connect(self):
# #         communicator = WebsocketCommunicator(
# #             AGameRoomConsumer.as_asgi(),
# #             f"/ws/pong/{self.room_id}/",
# #         )

# #         # 대충 인증 했다고 가정
# #         communicator.scope["user"] = await sync_to_async(User.objects.get)(
# #             email=TEST_USER_DATA["email"]
# #         )

# #         connected, _ = await communicator.connect()

# #         self.assertTrue(connected)
