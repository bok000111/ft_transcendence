# views.py
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
# Replace with the correct path to TournamentResult
from result.result import TournamentResult
from result.deploy import TournamentResultManager
from api.utils import AJsonMixin
import os


tournament_contract = TournamentResultManager(os.getenv("GANACHE_URL"))


class TournamentResultView(AJsonMixin, View):
    async def get(self, request):
        user = await request.auser()
        raw_datas = tournament_contract.get_all_tournaments()
        results = [TournamentResult(raw_data) for raw_data in raw_datas]
        results.sort(key=lambda x: x.timestamp)

        return JsonResponse([result.to_dict() for result in results], encoder=DjangoJSONEncoder, safe=False)
