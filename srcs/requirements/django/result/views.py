# views.py
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
# Replace with the correct path to TournamentResult
from result import TournamentResult
from deploy import TournamentResultManager
from api.utils import AJsonMixin
import os


tournament_contract = TournamentResultManager(
    "../../blockchain/TournamentContract.sol", os.getenv("GANACHE_URL"))


class TournamentResultView(AJsonMixin, View):
    def get(self, request):
        raw_datas = tournament_contract.get_results()
        results = [TournamentResult(raw_data) for raw_data in raw_datas].sort(
            key=lambda x: x.timestamp)
        return JsonResponse([result.to_dict() for result in results], encoder=DjangoJSONEncoder, safe=False)
