from django.test import TestCase, Client
from django.urls import reverse
from .models import User

import json

TEST_USER_DATA = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword",
}

TEST_LOGIN_DATA = {
    "email": "test@example.com",
    "password": "testpassword",
}


class SignupTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")

    def test_signup_success(self):
        response = self.client.post(
            self.signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User created.")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, TEST_USER_DATA["email"])
        self.assertNotEqual(User.objects.get().password, TEST_USER_DATA["password"])
        self.assertTrue(
            User.check_password(User.objects.get(), TEST_USER_DATA["password"])
        )

    def test_signup_failure(self):
        data = {"email": "", "username": "", "password": ""}
        response = self.client.post(
            self.signup_url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_signup_duplicated_email(self):
        response = self.client.post(
            self.signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )

        prev_count = User.objects.count()

        data = TEST_USER_DATA.copy()
        data["username"] = "testuser2"

        response = self.client.post(
            self.signup_url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Email is already in use.")
        self.assertEqual(prev_count, User.objects.count())

    def test_signup_duplicated_username(self):
        response = self.client.post(
            self.signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )

        prev_count = User.objects.count()

        data = TEST_USER_DATA.copy()
        data["email"] = "testuser2@example.com"

        response = self.client.post(
            self.signup_url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Username is already in use.")
        self.assertEqual(prev_count, User.objects.count())


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.signup_url = reverse("signup")

        self.client.post(
            self.signup_url, json.dumps(TEST_USER_DATA), content_type="application/json"
        )

    def test_login_success(self):
        response = self.client.post(
            self.login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logged in.")
        self.assertTrue(self.client.session["_auth_user_id"])

    def test_login_failure(self):
        data = TEST_LOGIN_DATA.copy()
        data["password"] = "wrongpassword"

        response = self.client.post(
            self.login_url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid credentials.")
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_login_already_logged_in(self):
        self.client.post(
            self.login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )
        self.assertTrue(self.client.session["_auth_user_id"])

        response = self.client.post(
            self.login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Already logged in.")


class LogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse("logout")
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")

        self.client.post(
            self.signup_url,
            json.dumps(TEST_USER_DATA),
            content_type="application/json",
        )

    def test_logout_success(self):
        self.client.post(
            self.login_url, json.dumps(TEST_LOGIN_DATA), content_type="application/json"
        )

        self.assertTrue(self.client.session["_auth_user_id"])

        response = self.client.post(self.logout_url, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logged out.")
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_logout_failure(self):
        response = self.client.post(self.logout_url, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Not logged in.")
