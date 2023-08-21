import  pygame

class GameManager:

    def __init__(self, game):
        self.game = game
        self.combo = 0
        self.prvElement = -1

    def mine(self, element):
        if self.prvElement == element:
            self.combo += 1
        else:
            self.combo = 0
        self.prvElement = element
        return

