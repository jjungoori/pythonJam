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


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Elemental Sky')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ui = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT))

        self.zoomFactor = 3
        self.player_speed = 1

        self.viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Define viewport here
        self.camPos = np.array((0,0), dtype=float)

        self.clock = pygame.time.Clock()
        self.movement = [False, False, False, False]

        self.assets = {
            'player/idle': Animation(load_images('entity/player'), img_dur=5),
        }
        self.tilemaps = {
            'main': StaticTilemap(
                Tileset(load_image("tileset/tileset.png"), size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH)),
            'object': StaticTilemap(
                Tileset(load_image("tileset/energy.png"), size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH))
        }

        self.player = Player(Animation(load_images('entity/player')), (5, 5)),
        self.particles = [

        ]
        self.objects = [

        ]
        self.tileObjects = [
            TileMine((14,8), self.tilemaps['object'], 'resources/map/tilemine.csv')
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

        targetZoom = self.zoomFactor


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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        for i in range(50):
                            self.particles.append(
                                Particle(self.player[0].center(), ((random.random() - 0.5) * 20, (random.random() - 0.5) * 20),
                                         5.0, random.random()+0.01, (random.random()*255, random.random()*255, random.random()*255), 0, 0))

                        # targetZoom += 0.5
                    elif event.key == pygame.K_w:
                        # self.UIs['textBox'].set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE, effect_tag='test')
                        self.tileObjects[0].mine()
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

            self.zoomFactor = (1 - CAM_LERP_SPEED * dt) * self.zoomFactor + CAM_LERP_SPEED * dt * targetZoom
            self.camPos = (1 - CAM_LERP_SPEED * dt) * self.camPos + CAM_LERP_SPEED * dt * self.player[0].pos

            self.viewport.left = self.camPos[1] - (SCREEN_HEIGHT / self.zoomFactor) / 2 + TILE_SIZE/2
            self.viewport.top = self.camPos[0] - (SCREEN_WIDTH / self.zoomFactor) / 2 + TILE_SIZE/2
            # self.viewport.width = SCREEN_WIDTH / self.zoomFactor
            # self.viewport.height = SCREEN_HEIGHT / self.zoomFactor

            for i in self.objects:
                i.update()
                i.render(self.display, self.viewport)
            for i in self.tilemaps:
                self.tilemaps[i].render(self.display, self.viewport)
            for i in self.particles:
                if i.update():
                    i.render(self.display, self.viewport, 1, 1)
                else:
                    self.particles.remove(i)

            self.player[0].update()
            self.player[0].render(self.display, self.viewport)

            capturedContent = self.display.copy()

            zoomedContent = pygame.transform.scale(capturedContent, (
            int(SCREEN_WIDTH * self.zoomFactor), int(SCREEN_HEIGHT * self.zoomFactor)))
            self.ui.update(dt)
            self.ui.draw_ui(zoomedContent)

            self.screen.blit(zoomedContent, (0, 0))
            # self.screen.blit(self.display, (0,0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    g = Game()
