# tests.py

import asyncio
import os
import random

from faker import Faker
from django.test import TransactionTestCase, AsyncClient
from django.urls import reverse

from ft_transcendence.tests import timer
from result.deploy import TournamentResultManager
from user.factories import UserFactory

faker = Faker()


def player_ids_generator(users, length=4, amount=100):
    for _ in range(amount):
        yield list(map(lambda user: user.pk, faker.random_elements(
            elements=users, unique=True, length=length)))


def tounament_result_generator(manager, users, amount=100):
    for pids in player_ids_generator(users, 4, amount):
        game_id = faker.random_int(1, 1000000000)
        game_time = faker.random_int(1600000000, 1718227200)

        left_win = [10, faker.random_int(0, 9)]
        right_win = [faker.random_int(0, 9), 10]

        yield manager.start_game, (game_id, game_time, pids)
        yield manager.save_sub_game, (game_id, [2, *random.choice([left_win, right_win])])
        yield manager.save_sub_game, (game_id, [3, *random.choice([left_win, right_win])])
        yield manager.save_sub_game, (game_id, [1, *random.choice([left_win, right_win])])


class TournamentResultTest(TransactionTestCase):

    def setUp(self):
        self.TEST_AMOUNT = 4
        self.client = AsyncClient()
        self.users = UserFactory.create_batch(self.TEST_AMOUNT)
        asyncio.run(self.asyncSetUp())

    async def asyncSetUp(self):
        self.manager = await TournamentResultManager.instance()

        # 로컬에서 실행시 블록체인 스냅샷 생성
        if os.getenv("HARDHAT_ENDPOINT"):
            response = await self.manager.w3.provider.make_request("evm_snapshot", [])
            self.snapshot_id = response["result"]

    def tearDown(self):
        # 블록체인 스냅샷 복구
        if os.getenv("HARDHAT_ENDPOINT"):
            asyncio.run(self.manager.w3.provider.make_request(
                "evm_revert", [self.snapshot_id]))
        TournamentResultManager._reset()

    async def test_transactions(self):
        game_id = faker.random_int(1, 1000000000)
        game_time = faker.random_int(1600000000, 1718227200)
        player_ids = player_ids_generator(self.users, 4, 1).__next__()

        left_win = [10, random.randint(0, 9)]
        right_win = [random.randint(0, 9), 10]
        random_win = [left_win, right_win]

        await self.manager.start_game(game_id, game_time, player_ids)
        await self.manager.save_sub_game(game_id, [2] + random_win[random.randint(0, 1)])
        await self.manager.save_sub_game(game_id, [3] + random_win[random.randint(0, 1)])
        await self.manager.save_sub_game(game_id, [1] + random_win[random.randint(0, 1)])

        await self.manager._wait_all()

    async def test_result_view(self):
        self.TEST_AMOUNT = 1
        response = await asyncio.gather(
            *[func(*args) for func, args in tounament_result_generator(self.manager, self.users, self.TEST_AMOUNT)]
        )

        await self.manager._wait_all()

        response = await self.client.get(reverse("result"), secure=True)

        # print(*(response.json()["data"]), sep="\n")

        self.assertContains(response, "success", status_code=200)
        if os.getenv("HARDHAT_ENDPOINT"):
            self.assertEqual(len(response.json()["data"]), self.TEST_AMOUNT)

    async def test_stress_transaction(self):
        response = await asyncio.gather(
            *[func(*args) for func, args in tounament_result_generator(self.manager, self.users, self.TEST_AMOUNT)]
        )

        await self.manager._wait_all()

        response = await self.client.get(reverse("result"), secure=True)
        self.assertContains(response, "success", status_code=200)
        if os.getenv("HARDHAT_ENDPOINT"):
            self.assertEqual(len(response.json()["data"]), self.TEST_AMOUNT)

    async def test_caching(self):
        response = await asyncio.gather(
            *[func(*args) for func, args in tounament_result_generator(self.manager, self.users, self.TEST_AMOUNT)]
        )

        await self.manager._wait_all()

        with timer("first request"):
            response = await self.client.get(reverse("result"), secure=True)
        self.assertContains(response, "success", status_code=200)
        if os.getenv("HARDHAT_ENDPOINT"):
            self.assertEqual(len(response.json()["data"]), self.TEST_AMOUNT)

        with timer("second request"):
            response = await self.client.get(reverse("result"), secure=True)
        self.assertContains(response, "success", status_code=200)
        if os.getenv("HARDHAT_ENDPOINT"):
            self.assertEqual(len(response.json()["data"]), self.TEST_AMOUNT)

        with timer("third request"):
            response = await self.client.get(reverse("result"), secure=True)
        self.assertContains(response, "success", status_code=200)
        if os.getenv("HARDHAT_ENDPOINT"):
            self.assertEqual(len(response.json()["data"]), self.TEST_AMOUNT)
