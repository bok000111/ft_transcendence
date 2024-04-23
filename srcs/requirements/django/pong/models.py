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


class GameRoom(models.Model):
    id = models.AutoField(
        primary_key=True, unique=True, help_text="Unique identifier for the room"
    )
    name = models.CharField(max_length=32, help_text="Name of the room")
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        help_text="List of players in the room",
        blank=True,
        related_name="players",
        through="PlayerInGame",
    )
    player_count = models.IntegerField(
        default=0,
        help_text="Number of players in the room",
    )
    max_player = models.IntegerField(
        default=2,
        help_text="Maximum number of players in the room",
    )
    # 관전은 나중에 구현
    end_score = models.IntegerField(
        default=10,
        help_text="Maximum score to win the game",
    )
    duration = models.IntegerField(
        default=60,
        help_text="Duration of the game - in seconds",
    )
    ball_speed = models.IntegerField(
        default=5,
        help_text="Speed of the ball in the game",
    )
    is_playing = models.BooleanField(
        default=False,
        help_text="Is the game playing?",
    )
    is_finished = models.BooleanField(
        default=False,
        help_text="Is the game finished?",
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

    def __str__(self):
        return f"GameRoom: {self.id}"

    @staticmethod
    @database_sync_to_async
    @transaction.atomic
    def create_room(
        name: str,
        host,
        max_player: int = 2,
        end_score: int = 10,
        duration: int = 60,
        ball_speed: int = 5,
    ):
        [room, created] = GameRoom.objects.get_or_create(
            name=name,
        )

        if not created:
            return None

        room.max_player = max_player
        room.end_score = end_score
        room.duration = duration
        room.ball_speed = ball_speed

        PlayerInGame.objects.create(player=host, room=room, is_host=True)
        room.players.add(host)
        room.player_count = room.players.count()
        room.save()

        return room

    @database_sync_to_async
    def get_players(self):
        return self.players.all()

    @database_sync_to_async
    def get_players_name(self):
        return list(self.players.values_list("username", flat=True))

    @database_sync_to_async
    def get_player_count(self):
        return self.players.count()

    @database_sync_to_async
    def get_player(self, user):
        return self.players.get(player=user)

    @database_sync_to_async
    def get_host(self):
        return self.players.get(playeringame__is_host=True)


class PlayerInGame(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User ID",
    )
    room = models.ForeignKey(
        GameRoom,
        on_delete=models.CASCADE,
        help_text="Room ID",
    )
    score = models.IntegerField(default=0, help_text="Player's score")
    is_host = models.BooleanField(default=False, help_text="Is the player the host?")
    is_ready = models.BooleanField(default=False, help_text="Is the player ready?")

    @staticmethod
    @database_sync_to_async
    @transaction.atomic
    def create_player(player, room):
        player_in_game = PlayerInGame.objects.create(player=player, room=room)
        room.players.add(player)
        room.player_count = room.players.count()
        room.save()

        return player_in_game
