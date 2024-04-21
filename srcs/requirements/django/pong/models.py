from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from user.models import User


# Pong 게임의 플레이어 정보
class Player(models.Model):
    id = models.AutoField(
        primary_key=True, unique=True, help_text="Unique identifier"
    )  # 거의 안쓸듯
    uid = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="User ID"
    )  # 게임 진행중인 유저가 다른 게임에 참여할 수 없도록 하는게 좋을듯
    room_id = models.ForeignKey(
        "PongRoomData", on_delete=models.CASCADE, help_text="Room ID"
    )
    score = models.IntegerField(default=0, help_text="Player's score")


# 현재 진행중인 게임의 기본 정보
class PongRoomData(models.Model):
    id = models.AutoField(
        primary_key=True, unique=True, help_text="Unique identifier for the room"
    )
    players = models.ManyToManyField(Player, help_text="List of players in the room")


# 현재 진행중인 게임의 상세 정보
class PongRoomMeta(models.Model):
    id = models.OneToOneField(
        PongRoomData,
        on_delete=models.CASCADE,
        primary_key=True,
        unique=True,
        help_text="Unique identifier for the room",
    )
    size = models.IntegerField(
        default=0,
        help_text="Number of players in the room",
    )
    capacity = models.IntegerField(
        default=2,
        help_text="Maximum number of players",
    )  # 아마 2인, 4인만 가능할듯
    max_score = models.IntegerField(
        default=1,
        help_text="Maximum score to win the game",
    )
    ball_speed = models.IntegerField(
        default=5,
        help_text="Speed of the ball in the game",
    )
    start_time = models.DateTimeField(
        auto_now_add=True, help_text="Start time of the game"
    )
    end_time = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="End time of the game",
    )  # end_time이 None이 아니면 게임이 종료된 것으로 간주하고 PongMatchData에 저장


# 종료된 게임의 정보
class PongMatchData(models.Model):
    id = models.AutoField(
        primary_key=True, unique=True, help_text="Unique identifier for the match"
    )
    players = models.ManyToManyField(Player, help_text="List of players in the match")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
