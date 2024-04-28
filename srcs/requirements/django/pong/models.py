from django.db import models, transaction
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async


User = get_user_model()


class EndReason(models.TextChoices):
    SCORE = "score", "Score"
    DISCONNECT = "disconnect", "Disconnect"
    TIMEOUT = "timeout", "Timeout"
    OTHER = "other", "Other"


class GameLobby(models.Model):
    id = models.AutoField(primary_key=True, unique=True, help_text="Lobby ID")
    name = models.CharField(max_length=32, help_text="Lobby name")
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        help_text="Players in lobby",
        blank=True,
        related_name="players",
        through="PlayerInLobby",
    )
    player_count = models.IntegerField(
        default=0,
        help_text="Current player count in the lobby",
    )
    max_player = models.IntegerField(
        default=2,
        help_text="Maximum player count in the lobby",
    )
    end_score = models.IntegerField(
        default=10,
        help_text="Score to win the game",
    )
    is_playing = models.BooleanField(
        default=False,
        help_text="Is the game playing",
    )
    is_finished = models.BooleanField(
        default=False,
        help_text="Is the game finished",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Creation time of the room"
    )
    started_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="Start time of the game",
    )
    ended_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="End time of the game",
    )
    ended_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="room_ended_by",
        blank=True,
        null=True,
        default=None,
        help_text="Player who ended the match",
    )
    end_reason = models.CharField(
        choices=EndReason.choices,
        max_length=16,
        blank=True,
        null=True,
        default=None,
        help_text="Reason for the end of the match",
    )


class PlayerInLobby(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User ID",
    )
    lobby = models.ForeignKey(
        GameLobby,
        on_delete=models.CASCADE,
        help_text="Lobby ID",
    )
    score = models.IntegerField(default=0, help_text="Player's score")
    is_host = models.BooleanField(default=False, help_text="Is the player the host")
    is_ready = models.BooleanField(default=False, help_text="Is the player ready")

    class Meta:
        unique_together = ("player", "lobby")


# class GameRoom(models.Model):
#     id = models.AutoField(
#         primary_key=True, unique=True, help_text="Unique identifier for the room"
#     )
#     name = models.CharField(max_length=32, help_text="Name of the room")
#     players = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         help_text="List of players in the room",
#         blank=True,
#         related_name="players",
#         through="PlayerInGame",
#     )
#     player_count = models.IntegerField(
#         default=0,
#         help_text="Number of players in the room",
#     )
#     max_player = models.IntegerField(
#         default=2,
#         help_text="Maximum number of players in the room",
#     )
#     # 관전은 나중에 구현
#     end_score = models.IntegerField(
#         default=10,
#         help_text="Maximum score to win the game",
#     )
#     duration = models.IntegerField(
#         default=60,
#         help_text="Duration of the game - in seconds",
#     )
#     ball_speed = models.IntegerField(
#         default=5,
#         help_text="Speed of the ball in the game",
#     )
#     is_playing = models.BooleanField(
#         default=False,
#         help_text="Is the game playing?",
#     )
#     is_finished = models.BooleanField(
#         default=False,
#         help_text="Is the game finished?",
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True, help_text="Creation time of the room"
#     )
#     started_at = models.DateTimeField(
#         blank=True,
#         null=True,
#         default=None,
#         help_text="Start time of the game",
#     )
#     ended_at = models.DateTimeField(
#         blank=True,
#         null=True,
#         default=None,
#         help_text="End time of the game",
#     )
#     ended_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="room_ended_by",
#         blank=True,
#         null=True,
#         default=None,
#         help_text="Player who ended the match",
#     )
#     end_reason = models.CharField(
#         choices=EndReason.choices,
#         max_length=16,
#         blank=True,
#         null=True,
#         default=None,
#         help_text="Reason for the end of the match",
#     )

#     def __str__(self):
#         return f"GameRoom: {self.id}"

#     @staticmethod
#     @database_sync_to_async
#     @transaction.atomic
#     def create_room(
#         name: str,
#         host,
#         max_player: int = 2,
#         end_score: int = 10,
#         duration: int = 60,
#         ball_speed: int = 5,
#     ):
#         room = GameRoom(
#             name=name,
#             max_player=max_player,
#             end_score=end_score,
#             duration=duration,
#             ball_speed=ball_speed,
#         )
#         room.save()

#         PlayerInGame.objects.create(player=host, room=room, is_host=True)
#         room.players.add(host)
#         room.player_count = room.players.count()
#         room.save()

#         return room

#     @database_sync_to_async
#     @transaction.atomic
#     def join_user(self, user) -> tuple[True, int, None] | tuple[False, int, str]:
#         if self.is_playing:
#             return [False, 400, "Game already started"]
#         elif self.players.count() >= self.max_player:
#             return [False, 400, "Game is full"]
#         elif self.players.filter(id=user.id).exists():
#             return [False, 400, "Already joined"]
#         elif self.is_finished:
#             return [False, 400, "Game already finished"]

#         player = PlayerInGame(player=user, room=self)
#         player.save()
#         self.players.add(user)
#         self.player_count = self.players.count()
#         self.save()
#         return [True, 200, None]

#     @database_sync_to_async
#     @transaction.atomic
#     def leave_user(self, user) -> tuple[True, int, None] | tuple[False, int, str]:
#         if self.is_playing:
#             return [False, 400, "Game already started"]
#         elif self.is_finished:
#             return [False, 400, "Game already finished"]
#         elif self.players.count() <= 1:
#             self.delete()
#             return [True, 200, None]
#         elif not self.players.filter(id=user.id).exists():
#             return [False, 400, "Not joined yet"]

#         player = PlayerInGame.objects.get(player=user, room=self)
#         if player.is_host:
#             new_host = self.players.exclude(id=user.id).first()
#             new_host.playeringame.is_host = True
#             new_host.playeringame.save()
#         player.delete()
#         self.players.remove(user)
#         self.player_count = self.players.count()
#         self.save()
#         return [True, 200, None]

#     @database_sync_to_async
#     def get_players(self):
#         return self.players.all()

#     @database_sync_to_async
#     def get_players_name(self):
#         return list(self.players.values_list("username", flat=True))

#     @database_sync_to_async
#     def get_player_count(self):
#         return self.players.count()

#     @database_sync_to_async
#     def get_player(self, user):
#         return self.players.get(player=user)

#     @database_sync_to_async
#     def get_host(self):
#         return self.players.get(playeringame__is_host=True)


# class PlayerInGame(models.Model):
#     player = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         help_text="User ID",
#     )
#     room = models.ForeignKey(
#         GameRoom,
#         on_delete=models.CASCADE,
#         help_text="Room ID",
#     )
#     score = models.IntegerField(default=0, help_text="Player's score")
#     is_host = models.BooleanField(default=False, help_text="Is the player the host?")
#     is_ready = models.BooleanField(default=False, help_text="Is the player ready?")

#     class Meta:
#         unique_together = ("player", "room")

#     @staticmethod
#     @database_sync_to_async
#     @transaction.atomic
#     def create_player(player, room):
#         player_in_game = PlayerInGame.objects.create(player=player, room=room)
#         room.players.add(player)
#         room.player_count = room.players.count()
#         room.save()

#         return player_in_game
