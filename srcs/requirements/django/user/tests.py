from django.test import TransactionTestCase, Client, AsyncClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async, async_to_sync

from concurrent.futures import ThreadPoolExecutor
from django.db import close_old_connections


import asyncio
import json
import time

User = get_user_model()

signup_url = reverse("signup")
login_url = reverse("login")
logout_url = reverse("logout")

TEST_USER_DATA = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword",
}

TEST_LOGIN_DATA = {
    "email": "test@example.com",
    "password": "testpassword",
}


class RequireJsonTest(TransactionTestCase):
    async def test_require_json_success(self):
        response = await self.async_client.post(
            reverse("signup"),
            json.dumps(TEST_USER_DATA),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    async def test_require_json_failure(self):
        response = await self.async_client.post(reverse("signup"))
        self.assertEqual(response.status_code, 400)


class SignupTest(TransactionTestCase):
    async def test_signup_success(self):
        response = await self.async_client.post(
            signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User created")
        self.assertEqual(await User.objects.acount(), 1)

        user = await User.objects.aget()

        self.assertEqual(user.email, TEST_USER_DATA["email"])
        self.assertNotEqual(user.password, TEST_USER_DATA["password"])
        self.assertTrue(User.check_password(user, TEST_USER_DATA["password"]))

    async def test_signup_failure(self):
        responses = await asyncio.gather(
            *[
                self.async_client.post(
                    signup_url, json.dumps(tc), content_type="application/json"
                )
                for tc in [
                    {**TEST_USER_DATA, "email": ""},
                    {**TEST_USER_DATA, "username": ""},
                    {**TEST_USER_DATA, "password": ""},
                ]
            ]
        )
        self.assertEqual([r.status_code for r in responses], [400, 400, 400])

    async def test_signup_duplicated_email(self):
        response = await self.async_client.post(
            signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )

        response = await self.async_client.post(
            signup_url,
            json.dumps({**TEST_USER_DATA, "username": "differentuser"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(await User.objects.acount(), 1)

    async def test_signup_duplicated_username(self):
        response = await self.async_client.post(
            signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )

        response = await self.async_client.post(
            signup_url,
            json.dumps({**TEST_USER_DATA, "email": "diffrentemail@example.com"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(await User.objects.acount(), 1)


class LoginTest(TransactionTestCase):
    def setUp(self):
        self.async_client = AsyncClient()

        async_to_sync(self.async_client.post)(
            signup_url,
            json.dumps(TEST_USER_DATA),
            content_type="application/json",
        )

    async def test_login_success(self):
        response = await self.async_client.post(
            login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json()["message"], "Logged in")

    async def test_login_failure(self):
        response = await self.async_client.post(
            login_url,
            json.dumps({**TEST_LOGIN_DATA, "password": "wrong"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid credentials")
        self.assertFalse(self.async_client.session.get("_auth_user_id"))

    async def test_login_already_logged_in(self):
        await self.async_client.post(
            login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )
        self.assertTrue(self.async_client.session["_auth_user_id"])

        response = await self.async_client.post(
            login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["message"], "Already logged in")


class LogoutTest(TransactionTestCase):
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

    async def test_logout_success(self):
        response = await self.async_client.post(
            logout_url, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logged out")
        self.assertFalse(self.async_client.session.get("_auth_user_id"))

    async def test_logout_failure(self):
        await self.async_client.post(logout_url, content_type="application/json")

        response = await self.async_client.post(
            logout_url, content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["message"], "Not logged in")


# 병렬 테스트만 가능
# class UserStressTest(TransactionTestCase):
#     def setUp(self):
#         self.DUMMY_USER_COUNT = 100
#         self.clients = [
#             {
#                 "client": Client(),
#                 "user": {
#                     "email": f"test{i}@example.com",
#                     "username": f"user{i}",
#                     "password": f"password{i}",
#                 },
#             }
#             for i in range(self.DUMMY_USER_COUNT)
#         ]

#     def signup(self, user):
#         return (
#             user["client"]
#             .post(
#                 signup_url,
#                 json.dumps(user["user"]),
#                 content_type="application/json",
#             )
#             .status_code
#         )

#     def login(self, user):
#         return (
#             user["client"]
#             .post(
#                 login_url,
#                 json.dumps(
#                     {
#                         "email": user["user"]["email"],
#                         "password": user["user"]["password"],
#                     }
#                 ),
#                 content_type="application/json",
#             )
#             .status_code
#         )

#     def logout(self, user):
#         return (
#             user["client"].post(logout_url, content_type="application/json").status_code
#         )

#     def tearDown(self):
#         super().tearDown()

#     async def test_signup_login_logout(self):
#         with ThreadPoolExecutor() as executor:
#             start = time.time()
#             signup_status = executor.map(
#                 self.signup,
#                 self.clients,
#             )
#             print(
#                 f"\nElapsed time for signup {self.DUMMY_USER_COUNT} users: {time.time() - start:.2f}s"
#             )
#             for status in signup_status:
#                 self.assertEqual(status, 201)

#             start = time.time()
#             login_status = executor.map(
#                 self.login,
#                 self.clients,
#             )
#             print(
#                 f"Elapsed time for login {self.DUMMY_USER_COUNT} users: {time.time() - start:.2f}s"
#             )
#             for status in login_status:
#                 self.assertEqual(status, 200)

#             start = time.time()
#             logout_status = executor.map(
#                 self.logout,
#                 self.clients,
#             )
#             print(
#                 f"Elapsed time for logout {self.DUMMY_USER_COUNT} users: {time.time() - start:.2f}s"
#             )
#             for status in logout_status:
#                 self.assertEqual(status, 200)

#         self.assertEqual(await User.objects.acount(), self.DUMMY_USER_COUNT)
