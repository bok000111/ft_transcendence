import threading
import time
import random
from .constants import *
from .player import Player


class AI_Player(Player):
    def __init__(self, idx, channel_name, nickname):
        super().__init__(idx, channel_name, nickname)
        self.ai = threading.Thread(target=self.ai_thread)
        self.ai.start()

    # def ai_thread(self):
    #     while True:
    #         time.sleep(0.1)
    #         if self.idx == 2:
    #             if random.random() < 0.5:
    #                 self.up = True
    #                 self.down = False
    #             else:
    #                 self.up = False
    #                 self.down = True
    #         elif self.idx == 3:
    #             if random.random() < 0.5:
    #                 self.up = False
    #                 self.down = True
    #             else:
    #                 self.up = True
    #                 self.down = False
    #         self.move()
