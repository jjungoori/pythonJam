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



class Game:
    def __init__(self):
        self.start = False

        self.renderer = Renderer(self)
        self.eventHandler = EventHandler(self)

        self.assets = {
            'player/idle': Animation(load_images('entity/player'), img_dur=10),
            'ui/elements': load_images('ui/elements'),
            'ui/leftBtn.png': 0,
            'ui/rightBtn.png': 0,
            'ui/scrollMask.png': 0,
            'ui/leftBtnPressed.png': 0,
            'ui/rightBtnPressed.png': 0,
            'ui/mine.png': 0,
            'ui/upgrade.png': 0,
            'ui/move.png': 0,
            'ui/UIBG.png' : 0,
            'ui/smallBtn.png' : 0,
            'ui/smallBtnPressed.png' : 0
            # 'ui/upgradeAdd' : 1
        }

        for i in self.assets:
            if self.assets[i] == 0:
                self.assets[i] = load_image(i)
            if i.startswith('ui/'):
                if i.endswith('.png'):
                    self.assets[i] = pygame.transform.scale(self.assets[i],
                                                            (self.assets[i].get_width() * 3,
                                                             self.assets[i].get_height() * 3))
                else:
                    for l in range(len(self.assets[i])):
                        self.assets[i][l] = pygame.transform.scale(self.assets[i][l],
                                                                (self.assets[i][l].get_width() * 3,
                                                                 self.assets[i][l].get_height() * 3))
                        self.assets[i][l].set_alpha(70)




        self.font = pygame.font.Font('resources/stardust.ttf')
        self.largeFont = pygame.font.Font('resources/stardust.ttf', 40)
        self.middleFont = pygame.font.Font('resources/stardust.ttf', 25)

        self.ui = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT))

        self.zoomFactor = 3
        self.player_speed = 1

        self.viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Define viewport here
        self.camPos = np.array((0,0), dtype=float)

        self.clock = pygame.time.Clock()
        self.movement = [False, False, False, False]


        self.soundAssets = {
            'mineSpawn' : pygame.mixer.Sound('resources/sound/mineSpawn.wav'),
            'mine' : pygame.mixer.Sound('resources/sound/mine.wav'),
            'mineSpawnStart' : pygame.mixer.Sound('resources/sound/mineSpawnStart.wav'),
            'jump' : pygame.mixer.Sound('resources/sound/jump.wav'),
            'fail50' : pygame.mixer.Sound('resources/sound/fail50.wav'),
            'fail200' : pygame.mixer.Sound('resources/sound/fail200.wav'),
            'change' : pygame.mixer.Sound('resources/sound/change.wav')
        }

        self.tilemaps = {
            'main': StaticTilemap(
                Tileset(load_image("tileset/tileset.png"), size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH)),
            'object': StaticTilemap(
                Tileset(load_image("tileset/energy.png"), size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH))
        }
        self.now = 0
        self.timer = Timer()
        self.player = Player(self.assets["player/idle"], tilePosToPos((14, 8))),
        self.particles = [

        ]
        self.objects = [

        ]
        self.tileObjects = [
            # getIsland('resources/map/basicIsland.json', self)
            # getTileMine('resources/map/basicTileMine.json', targetTilemap=self.tilemaps['object'], game=self)
            # Island((1,8), self.tilemaps['object'], 'resources/map/firstIsland.csv', (5,5), [])
        ]
        self.islands = [
            getIsland('resources/map/basicIsland.json', self),
            getIsland('resources/map/secondIsland.json', self)
        ]

        self.currentIslandIndex = 0
        self.currentIsland = self.islands[0]
        self.gameManager = GameManager(self)
        self.UIs = {
            # 'panel' : pygame_gui.elements.UIPanel(relative_rect = pygame.Rect(100,100,100,100), starting_height=1000, manager = self.ui),
            'button' : pygame_gui.elements.UIButton(relative_rect= (0,0), text = "hello", manager = self.ui),
            'textBox' : pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(100,100,100,50), html_text="hello", manager=self.ui),
        }

        self.renderer.run()
        self.load()
        self.run()


    def load(self):
        # self.tilemaps['main'].loadFromCsv('map/firstIsland.csv')

        for i in self.tileObjects:
            i.loadStructureFromCsv()
            i.placeOnTilemap()

        for i in self.islands:
            i.loadStructureFromCsv()
            i.placeOnTilemap()
            for l in i.objects:
                l.placeOnTilemap()

    def run(self):
        self.start = True
        prevTime = time.time()
        dragging = False
        lastUpdated = 0
        timeCounter = 0
        dt = 0

        pygame.mixer.music.load('resources/sound/bgm.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        while True:
            self.now = time.time()
            dt = self.now - prevTime
            prevTime = self.now
            timeCounter += dt

            self.timer.update()
            # Update logic here

            self.eventHandler.update()

            if self.movement[0]:
                self.player[0].pos[0] -= 1
            if self.movement[1]:
                self.player[0].pos[0] += 1
            if self.movement[2]:
                self.player[0].pos[1] -= 1
            if self.movement[3]:
                self.player[0].pos[1] += 1


            self.renderer.render(self, dt)
            self.now+=self.clock.tick(60)


if __name__ == "__main__":
    g = Game()
