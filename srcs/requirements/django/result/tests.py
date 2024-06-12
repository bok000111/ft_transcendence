# tests.py
from django.test import TestCase, AsyncClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from result.deploy import TournamentResultManager
from result.result import TournamentResult
import os

from user.factories import UserFactory

User = get_user_model()


class TournamentResultTest(TestCase):

    def setUp(self):
        self.exist_user = UserFactory()
        self.tournament_contract = TournamentResultManager(
            os.getenv("GANACHE_URL"))

    def test_tournament_flow(self):
        # Start the game
        self.tournament_contract.start_game(
            16, 1695940800, [263, 4516, 989, 1011])

        # Save sub games
        self.tournament_contract.save_sub_game(16, [2, 10, 1])
        self.tournament_contract.save_sub_game(16, [3, 2, 10])
        self.tournament_contract.save_sub_game(16, [1, 4, 10])

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
