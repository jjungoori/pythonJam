from scripts.renderer import *
from scripts.eventHandler import *
from scripts.gameManager import *
from scripts.assets import *
from scripts.UIManager import *



class Game:
    def __init__(self):

        pygame.init()
        self.renderer = Renderer(self)
        self.assets = Assets()
        self.eventHandler = EventHandler(self)
        self.gameManager = GameManager(self)
        self.UIManager = UIManager(self)
        self.timer = Timer()

        self.UIManager.run()

        # self.gameManager.newGame()
        self.gameManager.loadSave('testGameSave.pkl')
        self.gameManager.run()


if __name__ == "__main__":
    g = Game()
