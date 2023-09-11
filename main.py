from scripts.renderer import *
from scripts.eventHandler import *
from scripts.gameManager import *
from scripts.assets import *
from scripts.upgradeAdapter import *
from scripts.UIManager import *

import os.path
from os import path
from scripts.bossFight import *



class Game:
    def __init__(self):

        pygame.init()
        self.renderer = Renderer(self)
        self.assets = Assets()
        self.eventHandler = EventHandler(self)
        self.gameManager = GameManager(self)
        self.UIManager = UIManager(self)
        self.bossManager = BossManager(self)
        self.timer = Timer()
        self.UITimer = Timer()
        self.bossTimer = Timer()
        self.upgradeAdapter = UpgradeAdapter(self)

        self.UIManager.run()

        if path.exists('save.pkl'):
            self.gameManager.loadSave('save.pkl')
        else:
            self.gameManager.newGame()

        self.gameManager.run()
        self.bossManager.load()


if __name__ == "__main__":
    g = Game()
