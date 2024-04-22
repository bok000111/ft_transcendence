from django.test import TestCase, AsyncClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

# from concurrent.futures import ThreadPoolExecutor, as_completed

import asyncio
import json

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


class RequireJsonTest(TestCase):
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
        self.assertEqual(response.json()["message"], "Invalid content type.")


class SignupTest(TestCase):
    async def test_signup_success(self):
        response = await self.async_client.post(
            signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User created.")
        self.assertEqual(await User.objects.acount(), 1)

        user = await sync_to_async(User.objects.get)()

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
        self.assertEqual(
            [r.json()["message"] for r in responses],
            ["Email must be set", "Username must be set", "Password must be set"],
        )

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
        self.assertEqual(response.json()["message"], "Email is already in use.")
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
        self.assertEqual(response.json()["message"], "Username is already in use.")
        self.assertEqual(await User.objects.acount(), 1)


class LoginTest(TestCase):
    async def test_login_success(self):
        await self.async_client.post(
            signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )
        response = await self.async_client.post(
            login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logged in.")

    async def test_login_failure(self):
        await self.async_client.post(
            signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )
        response = await self.async_client.post(
            login_url,
            json.dumps({**TEST_LOGIN_DATA, "password": "wrong"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid credentials.")
        self.assertFalse(self.async_client.session.get("_auth_user_id"))

    async def test_login_already_logged_in(self):
        await self.async_client.post(
            signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )
        await self.async_client.post(
            login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )
        self.assertTrue(self.async_client.session["_auth_user_id"])

        response = await self.async_client.post(
            login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["message"], "Already logged in.")


class LogoutTest(TestCase):
    async def test_logout_success(self):
        await self.async_client.post(
            signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )
        await self.async_client.post(
            login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )

        self.assertTrue(self.async_client.session["_auth_user_id"])

        response = await self.async_client.post(
            logout_url, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logged out.")
        self.assertFalse(self.async_client.session.get("_auth_user_id"))

    async def test_logout_failure(self):

        response = await self.async_client.post(
            logout_url, content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["message"], "Not logged in.")


# 스레드풀 사용해서 동시성 테스트 하고싶었는데 안됨 몰라레후
# class UserStressTest(TestCase):
#     def setUp(self):
#         self.DUMMY_USER_COUNT = 10
#         self.test_users = [
#             {
#                 "email": f"test{i}@example.com",
#                 "username": f"user{i}",
#                 "password": f"password{i}",
#             }
#             for i in range(self.DUMMY_USER_COUNT)
#         ]

#     def stress_task(self, user):
#         return [
#             self.client.post(
#                 signup_url, json.dumps(user), content_type="application/json"
#             ).status_code,
#             self.client.post(
#                 login_url, json.dumps(user), content_type="application/json"
#             ).status_code,
#             self.client.post(logout_url, content_type="application/json").status_code,
#         ]

#     async def test_signup_login_logout(self):
#         with ThreadPoolExecutor() as executor:
#             result = as_completed(
#                 [executor.submit(self.stress_task, user) for user in self.test_users]
#             )
#             for future in result:
#                 self.assertEqual(future.result(), [201, 200, 200])

#         asyncio.sleep(1)

#         self.assertEqual(await User.objects.acount(), self.DUMMY_USER_COUNT)
