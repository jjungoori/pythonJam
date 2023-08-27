from scripts.utils import *
import numpy as np
from functools import partial

class UIManager:
    def __init__(self, game):
        self.interactiveUIs = 0
        self.actionImages = []
        self.game = game
        self.menuIndex = 0
        self.menu = GameMenu(self.game, [])

        self.targetScrollOffset = 0
        self.scrollOffset = 0
        return

    def run(self):
        ti = self.game.assets.images['ui/mine.png']
        self.actionButton = ImageButton([self.game.assets.images['ui/mine.png'], self.game.assets.images['ui/mine.png']], colCenter(ti, bottom(ti, (0, 0))), self.game.UIManager.menu.changeAct, 'add')
        self.actionImages = [
            self.game.assets.images['ui/mine.png'],
            self.game.assets.images['ui/move.png'],
            self.game.assets.images['ui/upgrade.png'],
        ]

    def render(self, zoomedScreen):

        leftBtns = [self.game.assets.images['ui/leftBtn.png'], self.game.assets.images['ui/leftBtnPressed.png']]
        rightBtns = [self.game.assets.images['ui/rightBtn.png'], self.game.assets.images['ui/rightBtnPressed.png']]

        dummy = self.game.assets.images['ui/leftBtn.png']
        ti = leftBtns[self.game.eventHandler.left]
        zoomedScreen.blit(ti, colCenter(ti, bottom(ti, (0, 0))) + np.array((-130, -20)))
        ti = rightBtns[self.game.eventHandler.right]
        zoomedScreen.blit(ti, colCenter(ti, bottom(ti, (0, 0))) + np.array((130, -20)))
        # print(self.game.gameManager.action, len(self.actionImages))
        self.actionButton.image = self.actionImages[self.game.gameManager.action]
        ti = self.actionButton
        zoomedScreen.blit(ti.image, ti.start)

        # zoomedScreen.blit(self.game.assets.font.render("Elemental", True, (0,0,0)), (10,10))

        txt = self.game.assets.largeFont.render(str(self.game.gameManager.combo), True, (83, 87, 92))
        if self.game.gameManager.combo >= 1:
            ti = self.game.assets.images['ui/elements'][self.game.gameManager.prvElement]
            zoomedScreen.blit(ti, colCenter(txt, (0, 40)) + np.array((-40, 0)))
        zoomedScreen.blit(txt, colCenter(txt, (0, 40)))

        txt = self.game.assets.font.render("Combo", True, (180, 180, 180))
        zoomedScreen.blit(txt, colCenter(txt, (0, 80)))

        txt = self.game.assets.font.render(str(self.game.gameManager.fire), True, (200, 100, 100))
        zoomedScreen.blit(txt, np.array((20, 20)))
        txt = self.game.assets.font.render(str(self.game.gameManager.water), True, (100, 100, 200))
        zoomedScreen.blit(txt, np.array((20, 40)))
        txt = self.game.assets.font.render(str(self.game.gameManager.air), True, (92, 154, 159))
        zoomedScreen.blit(txt, np.array((20, 60)))
        txt = self.game.assets.font.render(str(self.game.gameManager.lightening), True, (160, 160, 100))
        zoomedScreen.blit(txt, np.array((20, 80)))

        if self.game.UIManager.menu.on:
            menu = self.game.UIManager.menu
            ti = self.game.assets.images['ui/UIBG.png']
            bgPos = center(ti, (0, 0)) - np.array((0, 50))
            zoomedScreen.blit(ti, bgPos)

            txt = self.game.assets.largeFont.render(menu.title, True, (255, 255, 255))
            zoomedScreen.blit(txt, colCenter(txt, bgPos) - np.array((0, 15)))

            # zoomedScreen.blit(txt, np.array((20, 80)))

            bgPos += np.array((0, 20))

            self.scrollOffset += (self.targetScrollOffset - self.scrollOffset) * 0.1
            scrollViewRect = pygame.Rect(bgPos[0], bgPos[1]+10, 400, 340)

            zoomedScreen.set_clip(scrollViewRect)
            yPosition = scrollViewRect.y + self.scrollOffset

            for i, item in enumerate(menu.items):
                itemHeight = item.render(zoomedScreen, (scrollViewRect.x, yPosition))
                yPosition += itemHeight

            zoomedScreen.set_clip(None)

    def uiEvent(self):

        rt = False

        a = self.actionButton.update(self.game.gameManager.action)
        if a[0]:
            rt = (True, a[1])

        for i in self.game.UIManager.menu.items:
            # print("this ca")
            if i.button == 0:
                continue
            a = i.button.update()
            if a[0]:
                # print(';;')
                rt = (True, a[1])
        # if

        return rt

class ImageButton:
    def __init__(self, images, pos, func, *args):
        self.images = images
        self.image = self.images[0]
        self.start = pos
        self.end = pos + np.array((self.image.get_width(), self.image.get_height()))
        self.func = func

    def fixColl(self):
        self.start = self.pos
        self.end = self.pos + np.array((self.image.get_width(), self.image.get_height()))
    def update(self, *args):
        mp = pygame.mouse.get_pos()
        if mp[0] < self.end[0] and mp[0] > self.start[0] and mp[1] < self.end[1] and mp[1] > self.start[1]:
            if len(args) > 0:
                self.func(args[0])
            else:
                self.func()
            self.image = self.images[1]
            return True, self.up

        return False, self.up

    def up(self):
        self.image = self.images[0]


class GameMenuItems:
    def __init__(self, game, image, button, title, description):
        self.game = game
        self.image = image
        self.button = button
        self.title = title
        self.description = description
        self.cost = [0, 0, 0, 0]

    def render(self, zoomedScreen, bgPos):
        txtHeight = 0

        txt = self.game.assets.middleFont.render(self.title, True, (220, 220, 220))
        zoomedScreen.blit(txt, bgPos + np.array((40, 20)))
        txtHeight += 40  # Adding height for title

        wrappedDescription = textWrap(self.description, self.game.assets.font, 200)
        for j, line in enumerate(wrappedDescription):
            txt = self.game.assets.font.render(line, True, (150, 150, 150))
            zoomedScreen.blit(txt, bgPos + np.array((40, 50 + j * 20)))
        txtHeight += (len(wrappedDescription) * 20 + 10)  # Adding height for description

        if self.button != 0:
            btnPos = bgPos + np.array((265, 55))
            self.button.pos = np.array(btnPos)
            self.button.fixColl()
            zoomedScreen.blit(self.button.image, btnPos)

            txt1 = self.game.assets.font.render(str(self.cost[0]), True, (200, 100, 100))
            txt1Pos = bgPos + np.array((40, txtHeight + 10))
            zoomedScreen.blit(txt1, txt1Pos)

            txt2 = self.game.assets.font.render(str(self.cost[1]), True, (100, 100, 200))
            txt2Pos = txt1Pos + np.array((txt1.get_width() + 10, 0))
            zoomedScreen.blit(txt2, txt2Pos)

            txt3 = self.game.assets.font.render(str(self.cost[2]), True, (92, 154, 159))
            txt3Pos = txt2Pos + np.array((txt2.get_width() + 10, 0))
            zoomedScreen.blit(txt3, txt3Pos)

            txt4 = self.game.assets.font.render(str(self.cost[3]), True, (160, 160, 100))
            txt4Pos = txt3Pos + np.array((txt3.get_width() + 10, 0))
            zoomedScreen.blit(txt4, txt4Pos)

            txtHeight += 60  # Adding height for button and cost

        return txtHeight


class GameMenu:
    def __init__(self, game, items):
        self.on = False
        self.game = game
        self.items = items
        self.title = ""

    def upgrade(self, *args):
        self.game.gameManager.currentIsland.upgrades[args[0]] += 1

    def temp(self, data, key, i):
        # print("dbg2 : ", data)
        # print(self.game.gameManager.water, data['costs'][key][1])
        # print(self.game.gameManager.fire >= data['costs'][key][0], self.game.gameManager.water >= data['costs'][key][1],
        #       self.game.gameManager.air >= data['costs'][key][2],
        #       self.game.gameManager.lightening >= data['costs'][key][3])
        if self.game.gameManager.fire >= data['costs'][key][0] and self.game.gameManager.water >= data['costs'][key][
            1] and self.game.gameManager.air >= data['costs'][key][2] and self.game.gameManager.lightening >= \
                data['costs'][key][3]:
            # print("k")
            self.game.gameManager.fire -= data['costs'][key][0]
            self.game.gameManager.water -= data['costs'][key][1]
            self.game.gameManager.air -= data['costs'][key][2]
            self.game.gameManager.lightening -= data['costs'][key][3]

            self.game.gameManager.currentIsland.currentObject.upgrade(i)
            self.updateFromMine(self.game.gameManager.currentIsland.currentObject)

    def changeAct(self, num):
        self.game.gameManager.changeAct()
        return


    def updateFromMine(self, mine):
        self.title = "Mine"
        self.items = [

        ]
        for i in mine.upgrades:
            data = self.game.gameManager.mineUpgrades[i]

            key = mine.upgrades[i]
            temp = partial(self.temp, data, key, i)

            if len(data['costs']) - 1 > key:
                if self.game.gameManager.fire >= data['costs'][key][0] and self.game.gameManager.water >= data['costs'][key][1] and self.game.gameManager.air >= data['costs'][key][2] and self.game.gameManager.lightening >= data['costs'][key][3]:
                    btn = ImageButton([self.game.assets.images['ui/smallBtn.png'], self.game.assets.images['ui/smallBtnPressed.png']],
                                      (0, 0), temp)
                else:
                    btn = ImageButton([self.game.assets.images['ui/smallBtnPressed.png'], self.game.assets.images['ui/smallBtnPressed.png']],
                                      (0, 0), temp)

            else:
                btn = 0

            gmi = GameMenuItems(self.game, data['image'],
                                            btn, data['title'],
                                            data['descriptions'][key])
            gmi.cost = data['costs'][key]
            self.items.append(gmi)

    def updateFromIsland(self, island):
        self.title = "Island"
        self.items = [

        ]
        for i in island.upgrades:
            data = self.game.gameManager.mineUpgrades[i]
            # print("dbg : ", data)
            key = island.upgrades[i]
            temp = partial(self.temp, data, key, i)
            # def temp():
            #     print("dbg2 : ", data)
            #     print(self.game.gameManager.water, data['costs'][key][1])
            #     print(self.game.gameManager.fire >= data['costs'][key][0], self.game.gameManager.water >= data['costs'][key][1], self.game.gameManager.air >= data['costs'][key][2], self.game.gameManager.lightening >= data['costs'][key][3])
            #     if self.game.gameManager.fire >= data['costs'][key][0] and self.game.gameManager.water >= data['costs'][key][1] and self.game.gameManager.air >= data['costs'][key][2] and self.game.gameManager.lightening >= data['costs'][key][3]:
            #         print("k")
            #         self.game.gameManager.fire -= data['costs'][key][0]
            #         self.game.gameManager.water -= data['costs'][key][1]
            #         self.game.gameManager.air -= data['costs'][key][2]
            #         self.game.gameManager.lightening -= data['costs'][key][3]
            #
            #         self.game.gameManager.currentIsland.currentObject.upgrade(i)
            #         self.updateFromMine(self.game.gameManager.currentIsland.currentObject)

            if len(data['costs']) - 1 > key:
                if self.game.gameManager.fire >= data['costs'][key][0] and self.game.gameManager.water >= data['costs'][key][1] and self.game.gameManager.air >= data['costs'][key][2] and self.game.gameManager.lightening >= data['costs'][key][3]:
                    btn = ImageButton([self.game.assets.images['ui/smallBtn.png'], self.game.assets.images['ui/smallBtnPressed.png']],
                                      (0, 0), temp)
                else:
                    btn = ImageButton([self.game.assets.images['ui/smallBtnPressed.png'], self.game.assets.images['ui/smallBtnPressed.png']],
                                      (0, 0), temp)

            else:
                btn = 0

            gmi = GameMenuItems(self.game, data['image'],
                                            btn, data['title'],
                                            data['descriptions'][key])
            gmi.cost = data['costs'][key]
            self.items.append(gmi)