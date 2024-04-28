# from django.http import JsonResponse
# from django.views.generic import View
# from django.db.utils import IntegrityError
# from django.utils.decorators import method_decorator
# from channels.db import database_sync_to_async
# from asgiref.sync import sync_to_async
# import json

# from functools import partial

# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from user.utils import need_auth
# from api.utils import need_json

# from .models import GameLobby


# class GameRoomView(View):
#     @method_decorator(need_auth)
#     @method_decorator(csrf_exempt)
#     async def get(self, request, room_id):
#         room = await database_sync_to_async(GameRoom.objects.filter(id=room_id).first)()
#         if room is None:
#             return JsonResponse({"message": "Room not found"}, status=404)

#         host = await room.get_host()
#         players = await room.get_players_name()

#         return JsonResponse(
#             {
#                 "room_id": room.id,
#                 "name": room.name,
#                 "host": host.username,
#                 "max_players": room.max_player,
#                 "end_score": room.end_score,
#                 "duration": room.duration,
#                 "ball_speed": room.ball_speed,
#                 "player_count": room.player_count,
#                 "players": players,
#             },
#             status=200,
#         )


# @csrf_exempt
# @require_http_methods(["GET"])
# @need_auth
# async def room_by_id_view(_, room_id):
#     room = await database_sync_to_async(GameRoom.objects.filter(id=room_id).first)()
#     if room is None:
#         return JsonResponse({"message": "Room not found"}, status=404)

#     host = await room.get_host()
#     players = await room.get_players_name()

#     return JsonResponse(
#         {
#             "room_id": room.id,
#             "name": room.name,
#             "host": host.username,
#             "max_players": room.max_player,
#             "end_score": room.end_score,
#             "duration": room.duration,
#             "ball_speed": room.ball_speed,
#             "player_count": room.player_count,
#             "players": players,
#         },
#         status=200,
#     )


# @csrf_exempt
# @require_http_methods(["GET"])
# @need_auth
# async def room_list_view(request):
#     rooms = await database_sync_to_async(partial(list, GameRoom.objects.all()))()
#     rooms = [
#         {
#             "room_id": room.id,
#             "name": room.name,
#             "host": (await room.get_host()).username,
#             "max_players": room.max_player,
#             "end_score": room.end_score,
#             "duration": room.duration,
#             "ball_speed": room.ball_speed,
#             "player_count": room.player_count,
#         }
#         for room in rooms
#     ]
#     return JsonResponse({"rooms": rooms}, status=200)


# @csrf_exempt
# @require_http_methods(["POST"])
# @need_auth
# @need_json
# async def create_view(request):
#     data = json.loads(request.body)
#     name = data.get("name", None)
#     user = await request.auser()
#     max_players = data.get("max_players", 2)
#     end_score = data.get("end_score", 10)
#     duration = data.get("duration", 10)
#     ball_speed = data.get("ball_speed", 5)

#     if not name:
#         return JsonResponse({"message": "Invalid request"}, status=400)

#     room = await GameRoom.create_room(
#         name, user, max_players, end_score, duration, ball_speed
#     )
#     if not room:
#         return JsonResponse({"message": "Room already exists"}, status=400)
#     return JsonResponse({"message": "Room created", "room_id": room.id}, status=201)


# @csrf_exempt
# @require_http_methods(["POST"])
# @need_auth
# @need_json
# async def join_view(request):
#     data = json.loads(request.body)
#     room_id = data.get("room_id", None)
#     user = await request.auser()

#     if not room_id:
#         return JsonResponse({"message": "Invalid request"}, status=400)

#     room = await database_sync_to_async(GameRoom.objects.filter(id=room_id).first)()
#     if room is None:
#         return JsonResponse({"message": "Room not found"}, status=404)

#     try:
#         success, code, reason = await room.join_user(user)
#         if not success:
#             return JsonResponse({"message": reason}, status=code)
#         return JsonResponse({"message": "Joined room"}, status=200)
#     except IntegrityError:
#         return JsonResponse({"message": "Already joined"}, status=400)
#     except Exception as e:
#         return JsonResponse({"message": "Internal Error"}, status=500)


# @csrf_exempt
# @require_http_methods(["POST"])
# @need_auth
# @need_json
# async def leave_view(request):
#     data = json.loads(request.body)
#     room_id = data.get("room_id", None)
#     user = await request.auser()

#     if not room_id:
#         return JsonResponse({"message": "Invalid request"}, status=400)

#     room = await database_sync_to_async(GameRoom.objects.filter(id=room_id).first)()
#     if room is None:
#         return JsonResponse({"message": "Room not found"}, status=404)

#     try:
#         success, code, reason = await room.leave_user(user)
#         if not success:
#             return JsonResponse({"message": reason}, status=code)
#         return JsonResponse({"message": "Left room"}, status=200)
#     except IntegrityError:
#         return JsonResponse({"message": "Not joined yet"}, status=400)
#     except Exception as e:
#         return JsonResponse({"message": "Internal Error"}, status=500)
