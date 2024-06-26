import threading
import time
import random
from .constants import *
from .player import Player


class AI_Player(Player):
    def __init__(self, idx, uid, channel_name, nickname):
        super().__init__(idx, uid, channel_name, nickname)
