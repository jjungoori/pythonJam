import pygame

class Timer:
    def __init__(self):
        self.timers = []

    def add(self, delay, callback):
        execute_at = pygame.time.get_ticks() + delay
        self.timers.append((execute_at, callback))

    def update(self):
        current_time = pygame.time.get_ticks()
        for timer in self.timers.copy():
            execute_at, callback = timer
            if current_time >= execute_at:
                callback()
                self.timers.remove(timer)