from faker import Faker

from user.factories import UserFactory, SignUpFactory

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

signup_url = reverse("signup")
login_url = reverse("login")
logout_url = reverse("logout")


class RequireJsonTest(TestCase):
    async def test_require_json(self):
        response = await self.async_client.post(reverse("signup"))
        self.assertContains(response, "invalid content type", status_code=400)


class SignupTest(TransactionTestCase):
    def setUp(self):
        self.exist_user = UserFactory()

    def test_signup(self):
        data = SignUpFactory()
        response = self.client.post(signup_url, data, content_type="application/json")
        result = response.json()
        self.assertContains(response, "user created", status_code=201)
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

        self.assertContains(response, "logged in", status_code=200)
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

        self.assertContains(responses[0], "invalid credentials", status_code=400)
        self.assertContains(responses[1], "invalid credentials", status_code=400)

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

        self.assertContains(response, "already logged in", status_code=400)


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
        self.assertContains(response, "logged out", status_code=200)
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_logout_failure(self):
        self.client.post(logout_url, content_type="application/json")

        response = self.client.post(logout_url, content_type="application/json")
        self.assertContains(response, "authentication required", status_code=401)
