# pylint: disable=invalid-name, too-few-public-methods, unused-import


import asyncio
from typing import AsyncGenerator

from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase, Client, AsyncClient
from django.urls import reverse
from django.conf import settings

from user.tests import UserFactory
from ft_transcendence.asgi import application


User = get_user_model()


def channels_reverse(name, *args, **kwargs):

    return reverse(name, urlconf=settings.CHANNEL_URLCONF, args=args, kwargs=kwargs)


async def async_communicator_generator(
    signed: bool = False,
) -> AsyncGenerator[WebsocketCommunicator, None]:
    while True:
        headers = [(b"origin", "http://localhost".encode())]
        if signed:
            aclient = AsyncClient()
            await database_sync_to_async(lambda: aclient.force_login(UserFactory()))()
            headers.append(
                (b"cookie", aclient.cookies.output(header="", sep=";").encode())
            )
        yield WebsocketCommunicator(
            application,
            channels_reverse("main-ws"),
            headers=headers,
        )


class WebSocketTest(TransactionTestCase):
    TEST_AMOUNT = 5

    def setUp(self):
        self.user = UserFactory()
        self.client = AsyncClient()
        self.client.force_login(self.user)

    async def test_unauth_ws_connect(self):
        count = 0
        async for communicator in async_communicator_generator():
            connected, _ = await communicator.connect()
            self.assertFalse(connected)
            count += 1
            if count >= self.TEST_AMOUNT:
                break

    async def test_ws_connect(self):
        count = 0
        async for communicator in async_communicator_generator(True):
            connected, _ = await communicator.connect()
            self.assertTrue(connected)
            count += 1
            if count >= self.TEST_AMOUNT:
                break

    async def test_ws_join(self):
        communicators = []
        async for communicator in async_communicator_generator(True):
            await communicator.connect()
            await communicator.send_json_to(
                {
                    "action": "join",
                    "data": {"type": 0, "nickname": self.user.username},
                }
            )
            communicators.append(communicator)
            if len(communicators) >= self.TEST_AMOUNT:
                break

        for communicator in communicators:
            try:
                while True:
                    response = await communicator.receive_json_from()
                    print(response)
            except asyncio.TimeoutError:
                pass
            finally:
                await communicator.disconnect()
