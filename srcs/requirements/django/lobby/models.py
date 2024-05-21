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
    id = models.AutoField(primary_key=True, help_text="Lobby ID")
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
    max_players = models.IntegerField(
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

    @property
    @database_sync_to_async
    def is_full(self):
        return self.player_count >= self.max_players

    @property
    @database_sync_to_async
    def host(self):
        return self.players.filter(playerinlobby__is_host=True).first()

    @database_sync_to_async
    @transaction.atomic
    def join(self, user, nickname):
        self.players.add(user, through_defaults={"nickname": nickname})
        self.player_count += 1
        self.save()

    @database_sync_to_async
    @transaction.atomic
    def leave(self, user):
        self.players.remove(user)
        self.player_count -= 1
        self.save()


class PlayerInLobby(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User ID",
        # unique=True,
    )
    lobby = models.ForeignKey(
        GameLobby,
        on_delete=models.CASCADE,
        help_text="Lobby ID",
    )
    nickname = models.CharField(
        max_length=12,
        default="Default",
        help_text="Player's nickname in the lobby",
    )
    score = models.IntegerField(default=0, help_text="Player's score")
    is_host = models.BooleanField(default=False, help_text="Is the player the host")
    is_ready = models.BooleanField(default=False, help_text="Is the player ready")

    class Meta:
        unique_together = (
            ("lobby", "user"),
            ("lobby", "nickname"),
        )
