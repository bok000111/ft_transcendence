# pylint: disable=invalid-name, too-few-public-methods, unused-import


import asyncio
from functools import reduce
from asgiref.sync import async_to_sync, sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase, AsyncClient
from django.urls import reverse
from django.conf import settings
from faker import Faker

from user.tests import UserFactory
from ft_transcendence.asgi import application
from ft_transcendence.tests import timer


User = get_user_model()
faker = Faker()


def channels_reverse(name, *args, **kwargs):

    return reverse(name, urlconf=settings.CHANNEL_URLCONF, args=args, kwargs=kwargs)


async def build_communicator(user):
    headers = [(b"origin", b"http://localhost")]
    if user is not None:
        async_client = AsyncClient()
        await async_client.aforce_login(user)
        headers = [
            (b"origin", b"http://localhost"),
            (b"cookie", async_client.cookies.output(header="", sep=";").encode())
        ]
    return WebsocketCommunicator(
        application,
        channels_reverse("main-ws"),
        headers=headers,
    )


class WebSocketTest(TransactionTestCase):
    TEST_AMOUNT = 100

    def setUp(self):
        self.user = UserFactory()
        self.async_client = AsyncClient()
        self.async_client.force_login(self.user)
        self.users = UserFactory.create_batch(self.TEST_AMOUNT)

    def tearDown(self):
        faker.unique.clear()

    async def test_unauth_ws_connect(self):
        communicators = await \
            asyncio.gather(*[build_communicator(None)
                             for _ in range(self.TEST_AMOUNT)])

        with timer(f"reject {self.TEST_AMOUNT} unauthorized users"):
            for future in asyncio.as_completed(
                [communicator.connect(timeout=100)
                 for communicator in communicators]
            ):
                connected, _ = await future
                self.assertFalse(connected)

    async def test_ws_connect(self):
        communicators = await \
            asyncio.gather(*[build_communicator(user)
                             for user in self.users])

        with timer(f"connect {self.TEST_AMOUNT} users"):
            for future in asyncio.as_completed(
                [communicator.connect(timeout=100)
                 for communicator in communicators]
            ):
                connected, _ = await future
                self.assertTrue(connected)

    async def test_ws_join(self):
        communicators = await \
            asyncio.gather(*[build_communicator(user)
                             for user in self.users])
        await asyncio.gather(
            *[communicator.connect(timeout=100) for communicator in communicators]
        )

        with timer(f"join {self.TEST_AMOUNT} users"):
            await asyncio.gather(
                *[
                    communicator.send_json_to(
                        {
                            "action": "join",
                            "data": {
                                "type": faker.random_int(min=0, max=4),
                                "nickname": user.username,
                            },
                        }
                    )
                    for communicator, user in zip(communicators, self.users)
                ]
            )

        await asyncio.sleep(self.TEST_AMOUNT / 100.0)

        # with timer(f"receive {self.TEST_AMOUNT} responses"):
        #     for future in asyncio.as_completed(
        #         [communicator.receive_json_from()
        #          for communicator in communicators]
        #     ):
        #         response = await future
        #         print(response)

        # async def test_ws_join(self):
        #     with catchtime() as ct:
        #         await asyncio.gather(
        #             *[communicator.connect() for communicator in self.communicators]
        #         )

        #     with catchtime() as ct:
        #         await asyncio.gather(
        #             *[
        #                 communicator.send_json_to(
        #                     {
        #                         "action": "join",
        #                         "data": {
        #                             "type": faker.random_int(min=0, max=4),
        #                             "nickname": self.user.username,
        #                         },
        #                     }
        #                 )
        #                 for communicator in self.communicators
        #             ]
        #         )

        #     await asyncio.sleep(1)

        #     responses = await asyncio.gather(
        #         *[communicator.receive_json_from() for communicator in self.communicators]
        #     )

        #     print(*responses)

        # for communicator in communicators:
        #     try:
        #         while True:
        #             response = await communicator.receive_json_from()
        #             print(response)
        #     except asyncio.TimeoutError:
        #         pass
        #     finally:
        #         await communicator.disconnect()
