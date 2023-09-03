import random
import numpy as np
from scripts.utils import *


class Renderer:
    #tileObjects는 self.game 안에서 직접 로드. 프레임마다 재로드 불필요
    def __init__(self, game):
        pygame.display.set_caption('Elemental Sky')
        self.targetZoom = 3
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.shake = 10
        self.game = game
        # self.vignette = True
        # self.targetPos = self.game.gameManager.player.pos
        self.camTarget = 0 # 0 : player, 1 : free

    def render(self, dt):
        # self.screen.fill((0, 0, 0, 0))
        self.display.fill((201, 225, 229, 255))

        if self.camTarget == 0:
            self.targetPos = self.game.gameManager.player[0].pos

        # elif self.camTarget == 1:
        #     self.targetPos =

        # for i in self.game.gameManager.objects:
        #     i.update()
        #     i.render(self.display, self.game.gameManager.viewport)
        # for i in self.game.gameManager.tilemaps:
        #     self.game.gameManager.tilemaps[i].render(self.display,
        #                             self.game.gameManager.viewport)
        # self.screen.blit(self.display, (0, 0))



        self.game.gameManager.zoomFactor = (1 - CAM_LERP_SPEED * dt) * self.game.gameManager.zoomFactor + CAM_LERP_SPEED * dt * self.targetZoom
        self.game.gameManager.camPos = (1 - CAM_LERP_SPEED * dt) * self.game.gameManager.camPos + CAM_LERP_SPEED * dt * (self.targetPos + np.array((0,5)))

        self.game.gameManager.viewport.left = self.game.gameManager.camPos[1] - (SCREEN_HEIGHT / self.game.gameManager.zoomFactor) / 2 + TILE_SIZE / 2
        self.game.gameManager.viewport.top = self.game.gameManager.camPos[0] - (SCREEN_WIDTH / self.game.gameManager.zoomFactor) / 2 + TILE_SIZE / 2
        if self.shake > 0.1:
            self.game.gameManager.viewport.top += self.shake * (0.5 - random.random())
            self.game.gameManager.viewport.left += self.shake * (0.5 - random.random())
            self.shake *= 0.9

        for i in self.game.gameManager.tilemaps:
            self.game.gameManager.tilemaps[i].render(self.display, self.game.gameManager.viewport)
        for i in self.game.gameManager.objects:
            i.update()
            i.render(self.display, self.game.gameManager.viewport)
            # print(i)
        for i in self.game.gameManager.particles:
            if i.update():
                i.render(self.display, self.game.gameManager.viewport, 1, 1)
            else:
                self.game.gameManager.particles.remove(i)

        self.game.gameManager.player[0].update()
        self.game.gameManager.player[0].render(self.display, self.game.gameManager.viewport)

        capturedScreen = self.display.copy()

        zoomedScreen = pygame.transform.scale(capturedScreen, (
            int(SCREEN_WIDTH * self.game.gameManager.zoomFactor), int(SCREEN_HEIGHT * self.game.gameManager.zoomFactor)))
        # ------------------shader--------------
        # if self.vignette:
        #     zoomedScreen.blit(self.game.assets.vignette, bottom(self.game.assets.vignette, (0,0)))
        if self.game.UIManager.menu.on:
            translucentMask = pygame.Surface(zoomedScreen.get_size(), pygame.SRCALPHA)
            translucentColor = (0, 0, 0, 100)
            translucentMask.fill(translucentColor)
            zoomedScreen.blit(translucentMask, (0, 0))
        # ------------------UI------------------
        self.game.UIManager.render(zoomedScreen)
        #---------------------------------------
        self.screen.blit(zoomedScreen, (0, 0))
        pygame.display.update()

    def shakeScreen(self, intensity):
        if intensity > self.shake:
            self.shake = intensity

