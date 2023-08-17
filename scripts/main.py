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

        self.zoomFactor = 2
        self.player_speed = 1

        self.viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Define viewport here
        self.camPos = np.array((0,0), dtype=float)

        self.clock = pygame.time.Clock()
        self.movement = [False, False, False, False]

        self.assets = {
            'player/idle': Animation(load_images('entity/player'), img_dur=2),
        }
        self.tilemaps = {
            'main': StaticTilemap(
                Tileset(load_image("tileset/tileset.png"), self.zoomFactor, size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH)),
            'object': StaticTilemap(
                Tileset(load_image("tileset/energy.png"), self.zoomFactor, size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH))
        }

        self.player = GameObject(Animation(load_images('entity/player')), (5, 5)),

        self.objects = [

        ]

        self.load()
        self.run()

    def load(self):
        self.tilemaps['main'].loadFromCsv('../resources/map/firstIsland.csv')

    def run(self):
        prevTime = time.time()
        dragging = False
        lastUpdated = 0
        timeCounter = 0

        while True:
            self.screen.fill((0, 0, 0, 0))
            self.display.fill((0, 0, 0, 0))

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

            if self.movement[0]:
                self.player[0].pos[0] -= 1
            if self.movement[1]:
                self.player[0].pos[0] += 1
            if self.movement[2]:
                self.player[0].pos[1] -= 1
            if self.movement[3]:
                self.player[0].pos[1] += 1

            for i in self.objects:
                i.update()
                i.render(self.display, self.viewport)
            for i in self.tilemaps:
                self.tilemaps[i].render(self.display,
                                                self.viewport)
            self.screen.blit(self.display, (0,0))
            # zoomRect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            #
            # # Capture the area you want to zoom
            # capturedArea = self.screen.subsurface(zoomRect)
            #
            # # Scale the captured area based on the zoom factor
            # zoomedArea = pygame.transform.scale(capturedArea, (
            # int(zoomRect.width * self.zoomFactor), int(zoomRect.height * self.zoomFactor)))
            #
            # # Blit the zoomed area back to the screen at the desired position
            # self.screen.blit(zoomedArea, (zoomRect.left, zoomRect.top))

            self.camPos = (1 - CAM_LERP_SPEED * dt) * self.camPos + CAM_LERP_SPEED * dt * self.player[0].pos

            self.viewport.left = self.camPos[1] - (SCREEN_WIDTH / self.zoomFactor) / 2
            self.viewport.top = self.camPos[0] - (SCREEN_HEIGHT / self.zoomFactor) / 2
            self.viewport.width = SCREEN_WIDTH / self.zoomFactor
            self.viewport.height = SCREEN_HEIGHT / self.zoomFactor

            for i in self.objects:
                i.update()
                i.render(self.display, self.viewport)
            for i in self.tilemaps:
                self.tilemaps[i].render(self.display, self.viewport)
            self.player[0].update()
            self.player[0].render(self.display, self.viewport)

            capturedContent = self.display.copy()

            zoomedContent = pygame.transform.scale(capturedContent, (
            int(SCREEN_WIDTH * self.zoomFactor), int(SCREEN_HEIGHT * self.zoomFactor)))

            self.screen.blit(zoomedContent, (0, 0))

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game()
