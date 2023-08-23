import random
import  pygame
import numpy as np
import pygame
from scripts.constants import *
from scripts.utils import *


class Renderer:
    #tileObjects는 game 안에서 직접 로드. 프레임마다 재로드 불필요
    def __init__(self, game):
        pygame.init()
        pygame.display.set_caption('Elemental Sky')
        self.targetZoom = 3
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.shake = 10
        self.game = game

        self.interactiveUIs = {}

        self.actionImages = []
    def run(self):
        ti = self.game.assets['ui/mine.png']
        self.interactiveUIs['actionButton'] = (ImageButton([self.game.assets['ui/mine.png'], self.game.assets['ui/mine.png']], colCenter(ti, bottom(ti, (0,0))), self.game.gameManager.changeAct))
        self.actionImages = [
            self.game.assets['ui/mine.png'],
            self.game.assets['ui/move.png'],
            self.game.assets['ui/upgrade.png'],
        ]
    def render(self, game, dt):
        # self.screen.fill((0, 0, 0, 0))
        self.display.fill((201, 225, 229, 255))

        # for i in game.objects:
        #     i.update()
        #     i.render(self.display, game.viewport)
        # for i in game.tilemaps:
        #     game.tilemaps[i].render(self.display,
        #                             game.viewport)
        # self.screen.blit(self.display, (0, 0))

        game.zoomFactor = (1 - CAM_LERP_SPEED * dt) * game.zoomFactor + CAM_LERP_SPEED * dt * self.targetZoom
        game.camPos = (1 - CAM_LERP_SPEED * dt) * game.camPos + CAM_LERP_SPEED * dt * (game.player[0].pos + np.array((0,5)))

        game.viewport.left = game.camPos[1] - (SCREEN_HEIGHT / game.zoomFactor) / 2 + TILE_SIZE / 2
        game.viewport.top = game.camPos[0] - (SCREEN_WIDTH / game.zoomFactor) / 2 + TILE_SIZE / 2
        if self.shake > 0.1:
            game.viewport.top += self.shake * (0.5 - random.random())
            game.viewport.left += self.shake * (0.5 - random.random())
            self.shake *= 0.9

        for i in game.tilemaps:
            game.tilemaps[i].render(self.display, game.viewport)
        for i in game.objects:
            i.update()
            i.render(self.display, game.viewport)
            # print(i)
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
        # ------------------shader--------------
        if self.game.gameManager.menu.on:
            translucentMask = pygame.Surface(zoomedScreen.get_size(), pygame.SRCALPHA)
            translucentColor = (0, 0, 0, 100)
            translucentMask.fill(translucentColor)
            zoomedScreen.blit(translucentMask, (0, 0))
        # ------------------UI------------------

        leftBtns = [game.assets['ui/leftBtn.png'], game.assets['ui/leftBtnPressed.png']]
        rightBtns = [game.assets['ui/rightBtn.png'], game.assets['ui/rightBtnPressed.png']]

        dummy = game.assets['ui/leftBtn.png']
        ti = leftBtns[game.eventHandler.left]
        zoomedScreen.blit(ti, colCenter(ti, bottom(ti, (0,0))) + np.array((-130,-20) ))
        ti = rightBtns[game.eventHandler.right]
        zoomedScreen.blit(ti, colCenter(ti, bottom(ti, (0, 0))) + np.array((130,-20)))
        self.interactiveUIs['actionButton'].image = self.actionImages[self.game.gameManager.action]
        ti = self.interactiveUIs['actionButton']
        zoomedScreen.blit(ti.image, ti.start)

        # zoomedScreen.blit(game.font.render("Elemental", True, (0,0,0)), (10,10))

        txt = game.largeFont.render(str(game.gameManager.combo), True, (83, 87, 92))
        if game.gameManager.combo >= 1:
            ti = game.assets['ui/elements'][game.gameManager.prvElement]
            zoomedScreen.blit(ti, colCenter(txt, (0, 40)) + np.array((-40, 0)))
        zoomedScreen.blit(txt, colCenter(txt, (0,40)))

        txt = game.font.render("Combo", True, (180, 180, 180))
        zoomedScreen.blit(txt, colCenter(txt, (0, 80)))

        txt = game.font.render(str(game.gameManager.fire), True, (200, 100, 100))
        zoomedScreen.blit(txt,  np.array((20,20)))
        txt = game.font.render(str(game.gameManager.water), True, (100, 100, 200))
        zoomedScreen.blit(txt, np.array((20,40)))
        txt = game.font.render(str(game.gameManager.air), True, (90, 90, 120))
        zoomedScreen.blit(txt, np.array((20,60)))
        txt = game.font.render(str(game.gameManager.lightening), True, (160, 160, 100))
        zoomedScreen.blit(txt, np.array((20,80)))

        if self.game.gameManager.menu.on:
            menu = self.game.gameManager.menu
            ti = game.assets['ui/UIBG.png']
            bgPos = center(ti, (0,0)) -np.array((0,50))
            zoomedScreen.blit(ti, bgPos)
            bgPos += np.array((0, 20))

            for i in range(len(menu.items)):
                menuItem = menu.items[i]
                if menuItem.image:
                    ti = menuItem.image
                    zoomedScreen.blit(ti, bgPos + np.array((20,20 + 80*i)))
                txt = game.middleFont.render(menuItem.title, True, (220, 220, 220))
                zoomedScreen.blit(txt, bgPos + np.array((40,20 + 80*i)))

                txt = game.font.render(menuItem.description, True, (150, 150, 150))
                zoomedScreen.blit(txt, bgPos + np.array((40,50 + 80*i)))

                btnPos = bgPos + np.array((txt.get_width() + 50, 20 + 80*i))
                menuItem.button.pos = np.array(btnPos)
                menuItem.button.fixColl()
                zoomedScreen.blit(menuItem.button.image, btnPos)


                txt = game.font.render('+', True, (200, 0, 0))
                zoomedScreen.blit(txt, (192, 372))

        #---------------------------------------
        self.screen.blit(zoomedScreen, (0, 0))
        pygame.display.update()


    def uiEvent(self):

        rt = False

        for i in self.interactiveUIs:
            a = self.interactiveUIs[i].update()
            if a[0]:
                rt = (True, a[1])

        for i in self.game.gameManager.menu.items:
            print("this ca")
            a = i.button.update()
            if a[0]:
                print(';;')
                rt = (True, a[1])
        # if

        return rt

class ImageButton:
    def __init__(self, images, pos, func):
        self.images = images
        self.image = self.images[0]
        self.start = pos
        self.end = pos + np.array((self.image.get_width(), self.image.get_height()))
        self.func = func

    def fixColl(self):
        self.start = self.pos
        self.end = self.pos + np.array((self.image.get_width(), self.image.get_height()))
    def update(self):
        mp = pygame.mouse.get_pos()
        if mp[0] < self.end[0] and mp[0] > self.start[0] and mp[1] < self.end[1] and mp[1] > self.start[1]:
            self.func()
            self.image = self.images[1]
            return True, self.up

        return False, self.up

    def up(self):
        self.image = self.images[0]