# memory_game.py
import random
import time

class MemoryGame:
    def __init__(self):
        self.answer = [random.randint(1, 5) for _ in range(5)]
        self.user_input = []
        self.start_time = None
        self.status = 'waiting'  # 'showing', 'playing', 'win', 'fail'
        self.display_start = None
        self.input_number = 0

    def start(self):
        self.start_time = time.time()
        self.display_start = time.time()
        self.status = 'showing'

    def update(self):
        now = time.time()
        if self.status == 'showing' and now - self.display_start >= 3:
            self.start_time = now
            self.status = 'playing'
        elif self.status == 'playing' and now - self.start_time >= 10:
            self.status = 'fail'

    def handle_input(self, value):
        if self.status != 'playing':
            return
        self.user_input.append(value)
        if self.user_input != self.answer[:len(self.user_input)]:
            self.user_input = []
        elif len(self.user_input) == len(self.answer):
            self.status = 'win'

    def time_left(self):
        if self.status != 'playing':
            return 10.0
        return max(0.0, 10.0 - (time.time() - self.start_time))
