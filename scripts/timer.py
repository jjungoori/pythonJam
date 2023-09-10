import pygame

class Timer:
    def __init__(self):
        self.timers = []

    def add(self, delay, callback):
        targetTime = pygame.time.get_ticks() + delay
        self.timers.append((targetTime, callback, pygame.time.get_ticks()))

    def update(self):
        currentTime = pygame.time.get_ticks()
        for timer in self.timers.copy():
            targetTime, callback, _ = timer
            if currentTime >= targetTime:
                callback()
                if timer in self.timers:
                    self.timers.remove(timer)

    def remainingTimePercent(self, index):
        if index < len(self.timers):
            t = self.timers[index]

            return (t[0] - pygame.time.get_ticks())/(t[0] - t[2])