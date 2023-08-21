import pygame
import sys
from scripts.constants import *

class EventHandler:

    def __init__(self, game):
        self.game = game
        self.left = 0
        self.right = 0

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # self.game.movement[0] = True
                    self.leftC()
                elif event.key == pygame.K_RIGHT:
                    # self.game.movement[1] = True
                    self.rightC()
                elif event.key == pygame.K_UP:
                    self.game.movement[2] = True
                    pass
                elif event.key == pygame.K_DOWN:
                    self.game.movement[3] = True
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.up()
                if event.key == pygame.K_RIGHT:
                    self.up()
                if event.key == pygame.K_UP:
                    self.game.movement[2] = False
                    pass
                if event.key == pygame.K_DOWN:
                    self.game.movement[3] = False
                    pass
                if event.key == pygame.K_q:
                    self.game.tileObjects[0].spawnTileObject(self.game)

                    # targetZoom += 0.5
                elif event.key == pygame.K_w:
                    pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] <= SCREEN_WIDTH/2:
                    self.leftC()
                else:
                    self.rightC()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.up()
    def leftC(self):
        self.left = 1
        self.game.tileObjects[0].mine(0)
        # print(self.game.tileObjects[0].mine(0)[0])
    def up(self):
        self.right, self.left = 0, 0

    def rightC(self):
        self.right = 1
        self.game.tileObjects[0].mine(1)
        # print(self.game.tileObjects[0].mine(1)[0])