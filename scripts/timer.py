import pygame

class Timer:
    def __init__(self):
        self.timers = []

    def add(self, delay, callback):
        targetTime = pygame.time.get_ticks() + delay
        self.timers.append((targetTime, callback))

    def update(self):
        currentTime = pygame.time.get_ticks()
        for timer in self.timers.copy():
            targetTime, callback = timer
            if currentTime >= targetTime:
                callback()
                self.timers.remove(timer)