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



class Game:
    def __init__(self):

        self.renderer = Renderer()

        self.font = pygame.font.Font('resources/stardust.ttf')
        self.ui = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT))

        self.zoomFactor = 3
        self.player_speed = 1

        self.viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Define viewport here
        self.camPos = np.array((0,0), dtype=float)

        self.clock = pygame.time.Clock()
        self.movement = [False, False, False, False]

        self.assets = {
            'player/idle': Animation(load_images('entity/player'), img_dur=10),
            'ui/leftBtn.png' : 0,
            'ui/rightBtn.png' : 0
        }
        for i in self.assets:
            if self.assets[i] == 0:
                self.assets[i] = load_image(i)
            if i.startswith('ui/'):
                self.assets[i].


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
            TileMine((14,8), self.tilemaps['object'], 'resources/map/tilemine.csv', self)
        ]
        self.UIs = {
            # 'panel' : pygame_gui.elements.UIPanel(relative_rect = pygame.Rect(100,100,100,100), starting_height=1000, manager = self.ui),
            'button' : pygame_gui.elements.UIButton(relative_rect= (0,0), text = "hello", manager = self.ui),
            'textBox' : pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(100,100,100,50), html_text="hello", manager=self.ui),
        }

        self.load()
        self.run()


    def load(self):
        self.tilemaps['main'].loadFromCsv('map/firstIsland.csv')

        for i in self.tileObjects:
            i.loadStructureFromCsv()
            i.placeOnTilemap()

    def run(self):
        prevTime = time.time()
        dragging = False
        lastUpdated = 0
        timeCounter = 0
        dt = 0

        while True:
            self.now = time.time()
            dt = self.now - prevTime
            prevTime = self.now
            timeCounter += dt

            self.timer.update()
            # Update logic here

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    elif event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    elif event.key == pygame.K_UP:
                        self.movement[2] = True
                        pass
                    elif event.key == pygame.K_DOWN:
                        self.movement[3] = True
                        pass
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                        pass
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                        pass
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.tileObjects[0].spawnTileObject(self)

                        # targetZoom += 0.5
                    elif event.key == pygame.K_w:
                        # self.UIs['textBox'].set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE, effect_tag='test')
                        self.tileObjects[0].mine()
                        self.renderer.shake = 0.3
                        # targetZoom -= 0.5
                        pass
                self.ui.process_events(event)

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
