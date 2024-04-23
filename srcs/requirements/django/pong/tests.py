from django.test import AsyncClient, TransactionTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async, async_to_sync
from django.db import connection

import json

User = get_user_model()

signup_url = reverse("signup")
login_url = reverse("login")
logout_url = reverse("logout")

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
    "max_players": 4,
    "end_score": 5,
    "duration": 42,
    "ball_speed": 3,
}


class CreateRoomTest(TransactionTestCase):
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
        self.assertEqual(response.json()["message"], "Room created.")

    async def test_create_room_invalid_format(self):
        response = await self.async_client.post(
            create_room_url,
            json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid request.")

    async def test_create_room_dup_name(self):
        response = await self.async_client.post(
            create_room_url,
            json.dumps(TEST_ROOM_DATA),
            content_type="application/json",
        )
        response = await self.async_client.post(
            create_room_url,
            json.dumps({"name": "testroom"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Room already exists")


class GetRoomInfoTest(TransactionTestCase):
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

    def tearDown(self):
        async_to_sync(self.async_client.post)(logout_url)

    async def test_get_room_info_success(self):
        self.assertIsNotNone(self.room_id)
        response = await self.async_client.get(
            await sync_to_async(reverse)("get_room_by_id", args=[self.room_id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                **TEST_ROOM_DATA,
                "room_id": self.room_id,
                "host": TEST_USER_DATA["username"],
                "player_count": 1,
                "players": [TEST_USER_DATA["username"]],
            },
        )
