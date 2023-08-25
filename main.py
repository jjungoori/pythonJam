import random

import pygame
import pygame_gui
import sys
import numpy as np
import time
from scripts.tiles import *
from scripts.objects import *
from scripts.constants import *
from scripts.utils import *
from scripts.particle import *
from scripts.renderer import *
from  scripts.timer import *
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

        self.UIManager.run()
        self.gameManager.run()


if __name__ == "__main__":
    g = Game()
