# views.py
import os
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View

# Replace with the correct path to TournamentResult
from result.result import TournamentResult
from result.deploy import TournamentResultManager


class TournamentResultView(View):
    def get(self, request):
        raw_datas = TournamentResultManager(
            os.getenv("ENDPOINT")).get_all_tournaments()
        results = [TournamentResult(raw_data) for raw_data in raw_datas]
        results.sort(key=lambda x: x.timestamp)

        response_data = {
            "status": "success",
            "data": [result.to_dict() for result in results],
        }

        return JsonResponse(
            response_data,
            encoder=DjangoJSONEncoder,
            safe=False,
        )
