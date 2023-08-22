import  pygame

class GameManager:

    def __init__(self, game):
        self.game = game

        #for mines
        self.combo = 0
        self.prvElement = -1

        #for actions, 0 : mine, 1 : move, 2 : upgrade
        self.action = 0

        self.water = 0
        self.fire = 0
        self.lightening = 0
        self.cloud = 0

    def act(self, *args):
        if self.action == 0:
            self.game.tileObjects[0].mine(args[0])



    def mine(self, element):
        if self.prvElement == element:
            self.combo += 1
        else:
            self.game.soundAssets['fail50'].play()
            self.game.renderer.shake = self.combo/10
            self.combo = 0
        self.prvElement = element
        return

