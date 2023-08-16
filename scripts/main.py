import pygame
import sys
import numpy as np
import time
from tiles import *
from objects import *
from constants import *
from utils import *


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Elemental Sky')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.zoomFactor = 1
        self.player_speed = 1

        self.viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Define viewport here

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            'player/idle': Animation(load_images('resources/entity/player'), img_dur=2),
        }
        self.tilemaps = {
            'main': StaticTilemap(
                Tileset("resources/tileset/tileset.png", self.zoomFactor, size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH)),
            'object': StaticTilemap(
                Tileset("resources/tileset/energy.png", self.zoomFactor, size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH))
        }

        self.player = GameObject(Animation(load_images('resources/entity/player')), [5, 5]),

        self.objects = [

        ]

        self.load()
        self.run()

    def load(self):
        self.tilemaps['main'].loadFromCsv('resources/map/firstIsland.csv')

    def run(self):
        prevTime = time.time()
        dragging = False
        lastUpdated = 0
        timeCounter = 0

        while True:
            now = time.time()
            dt = now - prevTime
            prevTime = now
            timeCounter += dt
            # zoomedTileSize = TILE_SIZE * self.zoomFactor

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
                        # Add additional logic for the UP key here
                        pass
                    elif event.key == pygame.K_DOWN:
                        # Add additional logic for the DOWN key here
                        pass
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.player[0].update()
            self.player[0].render(self.screen, self.viewport)

            for i in self.objects:
                i.update()
                i.render(self.screen, self.viewport)
            for i in self.tilemaps:
                self.tilemaps[i].render(self.screen,
                                                self.viewport)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game()
