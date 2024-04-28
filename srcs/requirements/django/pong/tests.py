from django.test import AsyncClient, TransactionTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async, async_to_sync

from channels.auth import AuthMiddlewareStack
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from ft_transcendence.tests import login, logout, channels_reverse
from ft_transcendence.routing import urlpatterns

import asyncio
import json

User = get_user_model()

signup_url = reverse("signup")
login_url = reverse("login")
logout_url = reverse("logout")
get_room_list_url = reverse("get_room_list")
create_room_url = reverse("create_game_room")
join_room_url = reverse("join_game_room")
leave_room_url = reverse("leave_game_room")

create_room_url = reverse("create_game_room")

TEST_USER_DATA = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword",
}

TEST_LOGIN_DATA = {
    "email": "test@example.com",
    "password": "testpassword",
}

TEST_ROOM_DATA = {
    "name": "testroom",
    "max_players": 2,
    "end_score": 5,
    "duration": 42,
    "ball_speed": 3,
}


class GameRoomCreateTest(TransactionTestCase):
    def setUp(self):
        self.async_client = AsyncClient()

        async_to_sync(self.async_client.post)(
            signup_url,
            json.dumps(TEST_USER_DATA),
            content_type="application/json",
        )

        async_to_sync(self.async_client.post)(
            login_url,
            json.dumps(TEST_LOGIN_DATA),
            content_type="application/json",
        )

    def tearDown(self):
        async_to_sync(self.async_client.post)(logout_url)

    async def test_create_room_success(self):
        response = await self.async_client.post(
            create_room_url,
            json.dumps(TEST_ROOM_DATA),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Room created")

    async def test_create_room_invalid_format(self):
        response = await self.async_client.post(
            create_room_url,
            json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid request")

    async def test_create_room_invalid_name(self):
        response = await self.async_client.post(
            create_room_url,
            json.dumps({**TEST_ROOM_DATA, "name": ""}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid request")


class GameRoomModifyTest(TransactionTestCase):
    async def asyncSetUp(self):
        await asyncio.gather(
            *[
                client.post(
                    signup_url,
                    json.dumps(
                        {
                            **TEST_USER_DATA,
                            "email": f"test{i}@example.com",
                            "username": f"user{i}",
                        }
                    ),
                    content_type="application/json",
                )
                for i, client in enumerate(self.clients)
            ]
        )

        await asyncio.gather(
            *[
                client.post(
                    login_url,
                    json.dumps(
                        {
                            **TEST_LOGIN_DATA,
                            "email": f"test{i}@example.com",
                        }
                    ),
                    content_type="application/json",
                )
                for i, client in enumerate(self.clients)
            ]
        )

    def setUp(self):
        self.host = AsyncClient()

        async_to_sync(self.host.post)(
            signup_url,
            json.dumps(TEST_USER_DATA),
            content_type="application/json",
        )

        async_to_sync(self.host.post)(
            login_url,
            json.dumps(TEST_LOGIN_DATA),
            content_type="application/json",
        )

        response = async_to_sync(self.host.post)(
            create_room_url,
            json.dumps(TEST_ROOM_DATA),
            content_type="application/json",
        )
        self.room_id = response.json().get("room_id", None)

        self.clients = [AsyncClient() for _ in range(2)]

        async_to_sync(self.asyncSetUp)()

    def tearDown(self):
        async_to_sync(self.async_client.post)(logout_url)

    async def test_join_fail_leave(self):
        responses = await asyncio.gather(
            *[
                client.post(
                    reverse("join_game_room"),
                    json.dumps({"room_id": self.room_id}),
                    content_type="application/json",
                )
                for client in self.clients
            ]
        )

        self.assertEqual(200, responses[0].status_code)
        self.assertJSONEqual(
            responses[0].content,
            {"message": "Joined room"},
        )
        self.assertEqual(400, responses[1].status_code)
        self.assertJSONEqual(
            responses[1].content,
            {"message": "Game is full"},
        )

        responses = await asyncio.gather(
            *[
                client.post(
                    reverse("leave_game_room"),
                    json.dumps({}),
                    content_type="application/json",
                )
                for client in self.clients
            ]
        )

        response = await self.clients[0].get(
            reverse("get_room_by_id", args=[self.room_id])
        )

        self.assertEqual(200, response.status_code)
        print(response.content)

        responses = await asyncio.gather(
            *[
                client.post(
                    reverse("leave_game_room"),
                    json.dumps({}),
                    content_type="application/json",
                )
                for client in self.clients
            ]
        )

        self.assertEqual(200, responses[0].status_code)
        self.assertJSONEqual(
            responses[0].content,
            {"message": "Left room"},
        )
        self.assertEqual(400, responses[1].status_code)
        self.assertJSONEqual(
            responses[1].content,
            {"message": "Not in the room"},
        )


# class GetRoomInfoTest(TransactionTestCase):

#     async def AsetUp(self):
#         await asyncio.gather(
#             *[
#                 user["client"].post(
#                     signup_url,
#                     json.dumps(user["user"]),
#                     content_type="application/json",
#                 )
#                 for user in self.clients
#             ]
#         )

#         await asyncio.gather(
#             *[
#                 user["client"].post(
#                     login_url,
#                     json.dumps({**user["user"], "password": user["user"]["password"]}),
#                     content_type="application/json",
#                 )
#                 for user in self.clients
#             ]
#         )

#         self.room_ids = await asyncio.gather(
#             *[
#                 user["client"].post(
#                     create_room_url,
#                     json.dumps(TEST_ROOM_DATA),
#                     content_type="application/json",
#                 )
#                 for user in self.clients
#             ]
#         )

#         self.room_ids = [response.json()["room_id"] for response in self.room_ids]

#     def setUp(self):
#         self.DUMMY_USER_COUNT = 10
#         self.clients = [
#             {
#                 "client": AsyncClient(),
#                 "user": {
#                     "email": f"test{i}@example.com",
#                     "username": f"user{i}",
#                     "password": f"password{i}",
#                 },
#             }
#             for i in range(self.DUMMY_USER_COUNT)
#         ]
#         asyncio.run(self.AsetUp())

#     async def test_get_room_info(self):
#         responses = await asyncio.gather(
#             *[
#                 self.clients[0]["client"].get(
#                     await sync_to_async(reverse)("get_room_by_id", args=[room_id])
#                 )
#                 for room_id in self.room_ids
#             ]
#         )

#         self.assertTrue(all(response.status_code == 200 for response in responses))
#         self.assertTrue(
#             all(response.json().get("room_id", None) for response in responses)
#         )

#     async def test_get_room_list(self):
#         response = await self.clients[0]["client"].get(
#             await sync_to_async(reverse)("get_room_list")
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(response.json().get("rooms", None))


class RoomWebSocketTest(TransactionTestCase):
    async def asyncSetUp(self):
        self.cookies = await login(**TEST_LOGIN_DATA)

    def setUp(self):
        self.async_client = AsyncClient()

        async_to_sync(self.async_client.post)(
            signup_url,
            json.dumps(TEST_USER_DATA),
            content_type="application/json",
        )

        async_to_sync(self.async_client.post)(
            login_url,
            json.dumps(TEST_LOGIN_DATA),
            content_type="application/json",
        )

        response = async_to_sync(self.async_client.post)(
            create_room_url,
            json.dumps(TEST_ROOM_DATA),
            content_type="application/json",
        )
        self.room_id = response.json().get("room_id", None)

        asyncio.run(self.asyncSetUp())

    async def asyncTearDown(self):
        pass

    def tearDown(self):
        asyncio.run(self.asyncTearDown())

    async def test_ws_unauth(self):
        self.communicator = WebsocketCommunicator(
            AuthMiddlewareStack(URLRouter(urlpatterns)),
            f"/ws/pong/{self.room_id}/",
        )

        connected, code = await self.communicator.connect()

        self.assertFalse(connected)
        self.assertEqual(code, 403)

    async def test_ws_connect(self):
        self.communicator = WebsocketCommunicator(
            AuthMiddlewareStack(URLRouter(urlpatterns)),
            f"/ws/pong/{self.room_id}/",
            headers=[(b"cookie", self.cookies.output(header="", sep=";").encode())],
        )

        connected, subprotocol = await self.communicator.connect()

        self.assertTrue(connected)

        recv = await self.communicator.receive_json_from()
        assert recv["message"] == f"Connected to room {self.room_id}"

        await self.communicator.disconnect()


# class RoomWSTest(TransactionTestCase):
#     def setUp(self):
#         self.async_client = AsyncClient()

#         async_to_sync(self.async_client.post)(
#             signup_url,
#             json.dumps(TEST_USER_DATA),
#             content_type="application/json",
#         )

#         response = async_to_sync(self.async_client.post)(
#             login_url,
#             json.dumps(TEST_LOGIN_DATA),
#             content_type="application/json",
#         )
#         self.cookies = response.cookies

#         response = async_to_sync(self.async_client.post)(
#             create_room_url,
#             json.dumps(TEST_ROOM_DATA),
#             content_type="application/json",
#         )

#         self.room_id = response.json().get("room_id", None)

#     async def test_ws_connect(self):
#         communicator = WebsocketCommunicator(
#             AGameRoomConsumer.as_asgi(),
#             f"/ws/pong/{self.room_id}/",
#         )

#         # 대충 인증 했다고 가정
#         communicator.scope["user"] = await sync_to_async(User.objects.get)(
#             email=TEST_USER_DATA["email"]
#         )

#         connected, _ = await communicator.connect()

#         self.assertTrue(connected)
