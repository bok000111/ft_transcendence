import json
import time
from concurrent.futures import ThreadPoolExecutor

from faker import Faker

from django.test import TestCase, TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from user.factories import UserFactory, SignUpFactory
from api.utils import ModelJSONEncoder


User = get_user_model()

signup_url = reverse("signup")
login_url = reverse("login")
logout_url = reverse("logout")


class RequireJsonTest(TestCase):
    async def test_require_json(self):
        response = await self.async_client.post(reverse("signup"))
        self.assertContains(response, "Invalid content type", status_code=400)


class SignupTest(TransactionTestCase):
    def setUp(self):
        self.exist_user = UserFactory()

    def test_signup(self):
        data = SignUpFactory()
        response = self.client.post(signup_url, data, content_type="application/json")
        result = response.json()
        self.assertContains(response, "User created", status_code=201)
        self.assertQuerySetEqual(
            User.objects.filter(email=result["data"]["user"]["email"]),
            [data["email"]],
            lambda x: x.email,
        )
        self.assertQuerySetEqual(
            User.objects.filter(username=result["data"]["user"]["username"]),
            [data["username"]],
            lambda x: x.username,
        )
        self.assertTrue(
            User.check_password(
                User.objects.get(username=result["data"]["user"]["username"]),
                data["password"],
            )
        )

    def test_signup_failure(self):
        tcs = [
            SignUpFactory(email=""),
            SignUpFactory(username=""),
            SignUpFactory(password=""),
            SignUpFactory(email=self.exist_user.email),
            SignUpFactory(username=self.exist_user.username),
        ]

        responses = [
            self.client.post(signup_url, tc, content_type="application/json")
            for tc in tcs
        ]

        self.assertContains(responses[0], "Email required", status_code=400)
        self.assertContains(responses[1], "Username required", status_code=400)
        self.assertContains(responses[2], "Password required", status_code=400)
        self.assertContains(responses[3], "Email already exists", status_code=400)
        self.assertContains(responses[4], "Username already exists", status_code=400)


class LoginTest(TransactionTestCase):
    def setUp(self):
        self.password = Faker().password()
        self.user = UserFactory(
            password=self.password,
        )

    def test_login(self):
        response = self.client.post(
            login_url,
            {
                "email": self.user.email,
                "password": self.password,
            },
            content_type="application/json",
        )

        self.assertContains(response, "Logged in", status_code=200)
        self.assertTrue(self.client.session["_auth_user_id"])

    def test_login_failure(self):
        tcs = [
            {
                "email": self.user.email,
                "password": "wrong",
            },
            {
                "email": "wrong",
                "password": self.password,
            },
        ]

        responses = [
            self.client.post(login_url, tc, content_type="application/json")
            for tc in tcs
        ]

        self.assertContains(responses[0], "Invalid credentials", status_code=400)
        self.assertContains(responses[1], "Invalid credentials", status_code=400)

    def test_login_already_logged_in(self):
        self.client.post(
            login_url,
            {
                "email": self.user.email,
                "password": self.password,
            },
            content_type="application/json",
        )
        self.assertTrue(self.client.session["_auth_user_id"])

        response = self.client.post(
            login_url,
            {
                "email": self.user.email,
                "password": self.password,
            },
            content_type="application/json",
        )

        self.assertContains(response, "Already logged in", status_code=400)


class LogoutTest(TransactionTestCase):
    def setUp(self) -> None:
        password = Faker().password()
        self.user = UserFactory(
            password=password,
        )
        self.client.post(
            login_url,
            {
                "email": self.user.email,
                "password": password,
            },
            content_type="application/json",
        )

    def test_logout(self):
        response = self.client.post(logout_url, content_type="application/json")
        self.assertContains(response, "Logged out", status_code=200)
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_logout_failure(self):
        self.client.post(logout_url, content_type="application/json")

        response = self.client.post(logout_url, content_type="application/json")
        self.assertContains(response, "Not logged in", status_code=403)


# This test is for stress testing - need --parallel option
# class UserStressTest(TransactionTestCase):
#     def setUp(self):
#         faker = Faker()

#         self.DUMMY_USER_COUNT = 100
#         self.clients = [
#             {
#                 "client": Client(),
#                 "user": {
#                     "email": faker.unique.email(),
#                     "username": faker.unique.user_name(),
#                     "password": faker.password(),
#                 },
#             }
#             for _ in range(self.DUMMY_USER_COUNT)
#         ]

#     def signup(self, user):
#         response = user["client"].post(
#             signup_url,
#             user["user"],
#             cls=ModelJSONEncoder,
#             content_type="application/json",
#         )
#         if response.status_code == 201:
#             return 201
#         else:
#             print(response.json())

#     def login(self, user):
#         response = user["client"].post(
#             login_url,
#             {
#                 "email": user["user"]["email"],
#                 "password": user["user"]["password"],
#             },
#             content_type="application/json",
#         )
#         if response.status_code == 200:
#             return 200
#         else:
#             print(response.json())

#     def logout(self, user):
#         response = user["client"].post(
#             logout_url,
#             content_type="application/json",
#         )
#         if response.status_code == 200:
#             return 200
#         else:
#             print(response.json())

#     def test_signup_login_logout(self):
#         with ThreadPoolExecutor(max_workers=10) as executor:
#             start = time.time()
#             signup_status = executor.map(
#                 self.signup,
#                 self.clients,
#             )
#             for status in signup_status:
#                 self.assertEqual(status, 201)
#             signup_elapsed = time.time() - start

#             start = time.time()
#             login_status = executor.map(
#                 self.login,
#                 self.clients,
#             )
#             for status in login_status:
#                 self.assertEqual(status, 200)
#             login_elapsed = time.time() - start

#             start = time.time()
#             logout_status = executor.map(
#                 self.logout,
#                 self.clients,
#             )
#             for status in logout_status:
#                 self.assertEqual(status, 200)
#             logout_elapsed = time.time() - start
#         self.assertEqual(User.objects.count(), self.DUMMY_USER_COUNT)

#         print(
#             f"\nSignup: {signup_elapsed:.2f}s, Login: {login_elapsed:.2f}s, Logout: {logout_elapsed:.2f}s for {self.DUMMY_USER_COUNT} users"
#         )
