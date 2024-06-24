# tests.py
import os
import random

from django.test import TransactionTestCase, tag
from django.urls import reverse
from django.contrib.auth import get_user_model

from result.deploy import TournamentResultManager
from user.factories import UserFactory


class TournamentResultTest(TransactionTestCase):

    def setUp(self):
        self.fake_users = [UserFactory() for _ in range(4)]
        self.tournament_contract = TournamentResultManager(
            os.getenv("ENDPOINT"))

    @tag("slow")
    def test_tournament_flow(self):

        game_id = random.randint(1, 1000000000)
        game_time = random.randint(1600000000, 1718227200)
        player_ids = [user.pk for user in self.fake_users]
        print(player_ids)

        arr = [user.username for user in self.fake_users]
        print(arr)

        for i in player_ids:
            print(get_user_model().objects.get(pk=i).username)

        left_win = [10, random.randint(0, 9)]
        right_win = [random.randint(0, 9), 10]
        random_win = [left_win, right_win]

        # Start the game
        self.tournament_contract.start_game(game_id, game_time, player_ids)

        # Save sub games

        self.tournament_contract.save_sub_game(
            game_id, [2] + random_win[random.randint(0, 1)]
        )
        self.tournament_contract.save_sub_game(
            game_id, [3] + random_win[random.randint(0, 1)]
        )
        self.tournament_contract.save_sub_game(
            game_id, [1] + random_win[random.randint(0, 1)]
        )

        # Get all tournaments and print them
        tournaments = self.tournament_contract.get_all_tournaments()
        print(tournaments)
        # for res in tournaments:
        #     print(TournamentResult(res))

        # Assert the tournaments data
        self.assertTrue(len(tournaments) > 0)

    @tag("slow")
    def test_tournament_result_view(self):

        # Test the view
        response = self.client.get(reverse("result"), secure=True)
        self.assertContains(response, "", status_code=200)

        data = response.json()

        print(data)

        self.assertTrue(len(data) > 0)
