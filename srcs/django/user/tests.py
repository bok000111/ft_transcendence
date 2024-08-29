import asyncio
from asgiref.sync import sync_to_async
from user.factories import UserFactory, SignUpFactory, faker
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from ft_transcendence.tests import timer


class RequireJsonTest(TestCase):
    async def test_require_json(self):
        response = await self.async_client.post(
            reverse("signup"),
            secure=True,
        )
        self.assertContains(response, "invalid content type", status_code=400)


class SignupTest(TestCase):
    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        faker.unique.clear()
        cls.exist_user = UserFactory()

    async def test_signup(self):
        data = SignUpFactory()
        response = await self.async_client.post(
            reverse("signup"),
            data,
            content_type="application/json",
            secure=True,
        )
        result = response.json()
        self.assertContains(response, "user created", status_code=201)
        await sync_to_async(self.assertQuerySetEqual)(
            self.User.objects.filter(email=result["data"]["user"]["email"]),
            [data["email"]],
            lambda x: x.email,
        )
        await sync_to_async(self.assertQuerySetEqual)(
            self.User.objects.filter(
                username=result["data"]["user"]["username"]),
            [data["username"]],
            lambda x: x.username,
        )
        self.assertTrue(
            self.User.check_password(
                await self.User.objects.aget(username=result["data"]["user"]["username"]),
                data["password"],
            )
        )

    async def test_signup_failure(self):
        tcs = [
            SignUpFactory(email=""),
            SignUpFactory(username=""),
            SignUpFactory(password=""),
            SignUpFactory(email=self.exist_user.email),
            SignUpFactory(username=self.exist_user.username),
        ]

        responses = await asyncio.gather(
            *[
                self.async_client.post(
                    reverse("signup"),
                    tc,
                    content_type="application/json",
                    secure=True,
                )
                for tc in tcs
            ]
        )

        self.assertContains(responses[0], "Email required", status_code=400)
        self.assertContains(responses[1], "Username required", status_code=400)
        self.assertContains(responses[2], "Password required", status_code=400)
        self.assertContains(
            responses[3], "Email already exists", status_code=400)
        self.assertContains(
            responses[4], "Username already exists", status_code=400)


class LoginTest(TestCase):
    @ classmethod
    def setUpTestData(cls):
        faker.unique.clear()
        cls.email = faker.unique.email()
        cls.password = faker.unique.password()
        cls.user = UserFactory(
            email=cls.email,
            password=make_password(cls.password),
        )

    async def test_login(self):
        response = await self.async_client.post(
            reverse("login"),
            {
                "email": self.email,
                "password": self.password,
            },
            content_type="application/json",
            secure=True,
        )

        self.assertContains(response, "logged in", status_code=200)
        self.assertTrue(self.async_client.session["_auth_user_id"])

    async def test_login_failure(self):
        tcs = [
            {
                "email": self.email,
                "password": "wrong",
            },
            {
                "email": "wrong",
                "password": self.password,
            },
        ]

        responses = await asyncio.gather(
            *[
                self.async_client.post(
                    reverse("login"),
                    tc,
                    content_type="application/json",
                    secure=True,
                )
                for tc in tcs
            ]
        )

        self.assertContains(
            responses[0], "invalid credentials", status_code=400)
        self.assertContains(
            responses[1], "invalid credentials", status_code=400)

    async def test_login_already_logged_in(self):
        await self.async_client.aforce_login(self.user)

        response = await self.async_client.post(
            reverse("login"),
            {
                "email": self.email,
                "password": self.password,
            },
            content_type="application/json",
            secure=True,
        )

        self.assertContains(response, "already logged in", status_code=400)


class LogoutTest(TestCase):
    @ classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self) -> None:
        self.async_client.force_login(self.user)

    def tearDown(self) -> None:
        self.async_client.logout()

    async def test_logout(self):
        response = await self.async_client.post(
            reverse("logout"), content_type="application/json", secure=True
        )

        self.assertContains(response, "logged out", status_code=200)
        self.assertFalse(self.async_client.session.get("_auth_user_id"))

    async def test_logout_failure(self):
        await self.async_client.alogout()

        response = await self.async_client.post(
            reverse("logout"), content_type="application/json", secure=True
        )
        self.assertContains(
            response, "authentication required", status_code=401)


class StressTest(TransactionTestCase):
    TEST_AMOUNT = 10

    def setUp(self):
        self.users = [
            (SignUpFactory(), self.async_client_class())
            for _ in range(self.TEST_AMOUNT)
        ]
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    async def signup_login_logout(self, user, client):
        response = await client.post(
            self.signup_url, user, content_type="application/json", secure=True
        )
        self.assertContains(response, "user created", status_code=201)

        response = await client.post(
            self.login_url, user, content_type="application/json", secure=True,
        )
        self.assertContains(response, "logged in", status_code=200)

        response = await client.post(self.logout_url, content_type="application/json", secure=True)
        self.assertContains(response, "logged out", status_code=200)

    async def test_stress(self):

        with timer(f"signup login logout {self.TEST_AMOUNT} users"):
            await asyncio.gather(
                *[self.signup_login_logout(user, client) for user, client in self.users]
            )
