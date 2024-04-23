from django.http import JsonResponse
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from user.utils import need_auth
from api.utils import need_json

from .models import PlayerInGame, GameRoom


@csrf_exempt
@require_http_methods(["GET"])
@need_auth
async def by_id_view(request, room_id):
    room = await sync_to_async(GameRoom.objects.filter(id=room_id).first)()
    if room is None:
        return JsonResponse({"message": "Room not found."}, status=404)

    host = await room.get_host()
    players = await room.get_players_name()

    return JsonResponse(
        {
            "room_id": room.id,
            "name": room.name,
            "host": host.username,
            "max_players": room.max_player,
            "end_score": room.end_score,
            "duration": room.duration,
            "ball_speed": room.ball_speed,
            "player_count": room.player_count,
            "players": players,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["POST"])
@need_auth
@need_json
async def create_view(request):
    data = json.loads(request.body)
    name = data.get("name", None)
    user = await request.auser()
    max_players = data.get("max_players", 2)
    end_score = data.get("end_score", 10)
    duration = data.get("duration", 10)
    ball_speed = data.get("ball_speed", 5)

    if not name:
        return JsonResponse({"message": "Invalid request."}, status=400)

    room = await GameRoom.create_room(
        name, user, max_players, end_score, duration, ball_speed
    )
    if not room:
        return JsonResponse({"message": "Room already exists"}, status=400)
    return JsonResponse({"message": "Room created.", "room_id": room.id}, status=201)


# @csrf_exempt
# @require_http_methods(["POST"])
# def join_view(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({"message": "Not logged in."}, status=403)

#     data = json.loads(request.body)
#     room_id = data.get("room_id", None)

#     if not room_id:
#         return JsonResponse({"message": "Invalid request."}, status=400)

#     room = GameRoom.objects.filter(id=room_id).first()
#     if room is None:
#         return JsonResponse({"message": "Room not found."}, status=404)

#     with transaction.atomic():
#         if Player.objects.filter(user=request.user, room=room).exists():
#             return JsonResponse({"message": "Already joined."}, status=400)
#         Player.objects.create(user=request.user, room=room)

#     return JsonResponse({"message": "Joined room."}, status=200)


# @csrf_exempt
# @require_http_methods(["POST"])
# def leave_view(request):
#     pass


# @csrf_exempt
# @require_http_methods(["POST"])
# def ready_view(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({"message": "Not logged in."}, status=403)

#     data = json.loads(request.body)
#     room_id = data.get("room_id", None)

#     if not room_id:
#         return JsonResponse({"message": "Invalid request."}, status=400)

#     room = GameRoom.objects.filter(id=room_id).first()
#     if room is None:
#         return JsonResponse({"message": "Room not found."}, status=404)

#     player = Player.objects.filter(user=request.user, room=room).first()
#     if player is None:
#         return JsonResponse({"message": "Not joined."}, status=400)

#     player.is_ready = True
#     player.save()

#     return JsonResponse({"message": "Ready."}, status=200)
