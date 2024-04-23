from django.db.models.signals import post_save, pre_delete
from django.db import transaction
from django.dispatch import receiver

from .models import Player, Observer
from .models import GameRoom, GameRoomDetail, GameMatchData


@receiver(pre_delete, sender=GameRoom)
@transaction.atomic
def handle_game_room_delete(sender, instance, **kwargs):
    GameMatchData.create_match_data(room=instance)
