# views.py
from channels.db import database_sync_to_async
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View

from result.result import TournamentResult
from result.deploy import TournamentResultManager


class TournamentResultView(View):
    async def get(self, request):
        raw_datas = await (await TournamentResultManager.instance()).get_all_tournaments()
        results = await database_sync_to_async(
            lambda: [TournamentResult(raw_data) for raw_data in raw_datas]
        )()
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
