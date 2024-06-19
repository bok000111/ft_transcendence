# tests.py
from django.test import TestCase, AsyncClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from result.deploy import TournamentResultManager
from result.result import TournamentResult
import os
import random

from user.factories import UserFactory

User = get_user_model()


class TournamentResultTest(TestCase):

    def setUp(self):
        self.exist_user = UserFactory()
        self.tournament_contract = TournamentResultManager(
            os.getenv("ENDPOINT"))

    def test_tournament_flow(self):

        game_id = random.randint(1, 1000000000)
        game_time = random.randint(1600000000, 1718227200)
        player_ids = random.sample(range(1, 1000000000), 4)

        left_win = [10, random.randint(0, 9)]
        right_win = [random.randint(0, 9), 10]
        random_win = [left_win, right_win]

        # Start the game
        self.tournament_contract.start_game(
            game_id, game_time, player_ids)

        # Save sub games

        self.tournament_contract.save_sub_game(
            game_id, [2] + random_win[random.randint(0, 1)])
        self.tournament_contract.save_sub_game(
            game_id, [3] + random_win[random.randint(0, 1)])
        self.tournament_contract.save_sub_game(
            game_id, [1] + random_win[random.randint(0, 1)])

        # Get all tournaments and print them
        tournaments = self.tournament_contract.get_all_tournaments()
        print(tournaments)
        for res in tournaments:
            print(TournamentResult(res))

        # Assert the tournaments data
        self.assertTrue(len(tournaments) > 0)

    def test_tournament_result_view(self):

        # Test the view
        response = self.client.get(reverse('result'))
        self.assertContains(response, "", status_code=200)

        # You can also add more assertions to check the content of the response
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertIn('timestamp', data[0])
