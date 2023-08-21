import random

import numpy as np
import pygame
from scripts.constants import *
from scripts.utils import *


class Renderer:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Elemental Sky')
        self.targetZoom = 3
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.shake = 10

    def render(self, game, dt):
        # self.screen.fill((0, 0, 0, 0))
        self.display.fill((201, 225, 229, 255))

        for i in game.objects:
            i.update()
            i.render(self.display, game.viewport)
        for i in game.tilemaps:
            game.tilemaps[i].render(self.display,
                                    game.viewport)
        self.screen.blit(self.display, (0, 0))
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

        game.zoomFactor = (1 - CAM_LERP_SPEED * dt) * game.zoomFactor + CAM_LERP_SPEED * dt * self.targetZoom
        game.camPos = (1 - CAM_LERP_SPEED * dt) * game.camPos + CAM_LERP_SPEED * dt * (game.player[0].pos + np.array((0,5)))

        game.viewport.left = game.camPos[1] - (SCREEN_HEIGHT / game.zoomFactor) / 2 + TILE_SIZE / 2
        game.viewport.top = game.camPos[0] - (SCREEN_WIDTH / game.zoomFactor) / 2 + TILE_SIZE / 2
        if self.shake > 0.1:
            game.viewport.top += self.shake * (0.5 - random.random())
            game.viewport.left += self.shake * (0.5 - random.random())
            self.shake *= 0.9
        # self.viewport.width = SCREEN_WIDTH / self.zoomFactor
        # self.viewport.height = SCREEN_HEIGHT / self.zoomFactor

        for i in game.tilemaps:
            game.tilemaps[i].render(self.display, game.viewport)
        for i in game.objects:
            i.update()
            i.render(self.display, game.viewport)
        for i in game.particles:
            if i.update():
                i.render(self.display, game.viewport, 1, 1)
            else:
                game.particles.remove(i)

        game.player[0].update()
        game.player[0].render(self.display, game.viewport)

        capturedScreen = self.display.copy()

        zoomedScreen = pygame.transform.scale(capturedScreen, (
            int(SCREEN_WIDTH * game.zoomFactor), int(SCREEN_HEIGHT * game.zoomFactor)))
        # game.ui.update(dt)
        # game.ui.draw_ui(zoomedScreen)
        # ------------------UI------------------

        leftBtns = [game.assets['ui/leftBtn.png'], game.assets['ui/leftBtnPressed.png']]
        rightBtns = [game.assets['ui/rightBtn.png'], game.assets['ui/rightBtnPressed.png']]

        dummy = game.assets['ui/leftBtn.png']
        ti = leftBtns[game.eventHandler.left]
        zoomedScreen.blit(ti, colCenter(ti, bottom(ti, (0,0))) + np.array((-130,-20) ))
        ti = rightBtns[game.eventHandler.right]
        zoomedScreen.blit(ti, colCenter(ti, bottom(ti, (0, 0))) + np.array((130,-20)))
        ti = game.assets['ui/mine.png']
        zoomedScreen.blit(ti, colCenter(ti, bottom(ti, (0,0))))

        # zoomedScreen.blit(game.font.render("Elemental", True, (0,0,0)), (10,10))

        txt = game.largeFont.render(str(game.gameManager.combo), True, (83, 87, 92))
        if game.gameManager.combo >= 1:
            ti = game.assets['ui/elements'][game.gameManager.prvElement]
            # print(ti)
            zoomedScreen.blit(ti, colCenter(txt, (0, 40)) + np.array((-40, 0)))
        zoomedScreen.blit(txt, colCenter(txt, (0,40)))

        txt = game.font.render("Combo", True, (180, 180, 180))
        zoomedScreen.blit(txt, colCenter(txt, (0, 80)))

        #---------------------------------------
        self.screen.blit(zoomedScreen, (0, 0))
        # self.screen.blit(self.display, (0,0))
        pygame.display.update()