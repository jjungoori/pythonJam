from scripts.utils import *
import numpy as np
from functools import partial
from scripts.dialogManager import *
import copy

class UIManager:
    def __init__(self, game):
        self.interactiveUIs = 0
        self.actionImages = []
        self.game = game
        self.menuIndex = 0
        self.menu = GameMenu(self.game, [])
        self.dialog = Dialog(self.game)
        self.dialogManager = DialogManager(self.game)

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

        if self.game.gameManager.combo > 1000:
            txt = self.game.assets.font.render("COMBO!!! X 4", True, (83, 87, 92))
            zoomedScreen.blit(txt, colCenter(txt, (0, 110)))
        elif self.game.gameManager.combo > 500:
            txt = self.game.assets.font.render("COMBO!!! X 3", True, (83, 87, 92))
            zoomedScreen.blit(txt, colCenter(txt, (0, 110)))
        elif self.game.gameManager.combo > 100:
            txt = self.game.assets.font.render("COMBO!!! X 2", True, (83, 87, 92))
            zoomedScreen.blit(txt, colCenter(txt, (0, 110)))

        txt = self.game.assets.font.render(str(self.game.gameManager.fire), True, (200, 100, 100))
        zoomedScreen.blit(txt, np.array((20, 20)))
        txt = self.game.assets.font.render(str(self.game.gameManager.water), True, (100, 100, 200))
        zoomedScreen.blit(txt, np.array((20, 40)))
        txt = self.game.assets.font.render(str(self.game.gameManager.air), True, (92, 154, 159))
        zoomedScreen.blit(txt, np.array((20, 60)))
        txt = self.game.assets.font.render(str(self.game.gameManager.lightening), True, (160, 160, 100))
        zoomedScreen.blit(txt, np.array((20, 80)))




        txt = self.game.assets.font.render("Press Q to save!", True, (83, 87, 92))
        zoomedScreen.blit(txt, bottom(txt, (0,0)) + np.array((10,-10)))

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

        self.dialog.render(zoomedScreen)

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
        txtHeight += 40

        wrappedDescription = textWrap(self.description, self.game.assets.font, 200)
        for j, line in enumerate(wrappedDescription):
            txt = self.game.assets.font.render(line, True, (150, 150, 150))
            zoomedScreen.blit(txt, bgPos + np.array((40, 50 + j * 20)))
        txtHeight += (len(wrappedDescription) * 20 + 10)

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

            txtHeight += 60

        return txtHeight


class GameMenu:
    def __init__(self, game, items):
        self.on = False
        self.game = game
        self.items = items
        self.title = ""

    def upgrade(self, *args):
        self.game.gameManager.currentIsland.upgrades[args[0]] += 1

    def tempMine(self, data, key, i):
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

    def tempIsland(self, data, key, i):
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

            self.game.gameManager.currentIsland.upgrade(i)
            self.updateFromIsland(self.game.gameManager.currentIsland)

    def tempPlayer(self, cost, i):

        if self.game.gameManager.fire >= cost[0] and self.game.gameManager.water >= cost[
            1] and self.game.gameManager.air >= cost[2] and self.game.gameManager.lightening >= \
                cost[3]:
            # print("k")
            self.game.gameManager.fire -= cost[0]
            self.game.gameManager.water -= cost[1]
            self.game.gameManager.air -= cost[2]
            self.game.gameManager.lightening -= cost[3]

            self.game.gameManager.playerAtt.upgrades[i] += 1

            self.game.gameManager.playerAtt.adaptUpgrade()
            self.updateFromPlayer()


    def tempNewIsland(self, cost, island):
        # print("hhhh")
        if self.game.gameManager.fire >= cost[0] and self.game.gameManager.water >= cost[
            1] and self.game.gameManager.air >= cost[2] and self.game.gameManager.lightening >= cost[3]:
            # print("ggggg")

            island.foundNew = True
            self.game.gameManager.level += 1

            self.game.gameManager.fire -= cost[0]
            self.game.gameManager.water -= cost[1]
            self.game.gameManager.air -= cost[2]
            self.game.gameManager.lightening -= cost[3]

            self.updateFromNew(island)

            self.changeAct(2)
            self.game.timer.add(1, self.game.gameManager.spawnNewIsland)



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
            temp = partial(self.tempMine, data, key, i)

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
            temp = partial(self.tempIsland, data, key, i)

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

    def updateFromPlayer(self):
        self.title = "Player"
        self.items = [

        ]
        for i in self.game.gameManager.playerAtt.upgrades:
            data = []
            data = copy.deepcopy(self.game.gameManager.playerUpgrades[i])  #deepcopy
            # print("dbg : ", data)
            key = self.game.gameManager.playerAtt.upgrades[i]

            mul = 1
            if  data['infinity']:
                mul += key//len(data['costs'])
                pk = key
                key = key%len(data['costs'])-1
                print("key :", key)
                if key == -1:
                    mul = (pk+1)//(len(data['costs']))

                print(mul)
                for l in range(len(data['costs'][key])):
                    data['costs'][key][l] *= mul
                    print(data['costs'][key][l])

            temp = partial(self.tempPlayer, data['costs'][key], i)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if len(data['costs']) - 1 > key:
                if self.game.gameManager.fire >= data['costs'][key][0] and self.game.gameManager.water >= data['costs'][key][1] and self.game.gameManager.air >= data['costs'][key][2] and self.game.gameManager.lightening >= data['costs'][key][3]:
                    btn = ImageButton([self.game.assets.images['ui/smallBtn.png'], self.game.assets.images['ui/smallBtnPressed.png']],
                                      (0, 0), temp)
                else:
                    btn = ImageButton([self.game.assets.images['ui/smallBtnPressed.png'], self.game.assets.images['ui/smallBtnPressed.png']],
                                      (0, 0), temp)

            else:
                btn = 0

            gmi = GameMenuItems(self.game, 0,
                                            btn, data['title'],
                                            data['description'])
            gmi.cost = data['costs'][key]
            self.items.append(gmi)


    def updateFromNew(self, island):
        self.title = "New Island"
        self.items = [

        ]

        cost = [*map(lambda x : x * max(1, self.game.gameManager.level - len(ISLAND_COST) + 1), ISLAND_COST[min(self.game.gameManager.level, len(ISLAND_COST)-1)])]

        temp = partial(self.tempNewIsland, cost, island)

        des = "Get a new random island!"

        if not island.foundNew:
            if self.game.gameManager.fire >= cost[0] and self.game.gameManager.water >= \
                    cost[1] and self.game.gameManager.air >= cost[
                2] and self.game.gameManager.lightening >= cost[3]:
                btn = ImageButton(
                    [self.game.assets.images['ui/smallBtn.png'], self.game.assets.images['ui/smallBtnPressed.png']],
                    (0, 0), temp)
            else:
                btn = ImageButton([self.game.assets.images['ui/smallBtnPressed.png'],
                                   self.game.assets.images['ui/smallBtnPressed.png']],
                                  (0, 0), temp)

        else:
            btn = 0
            des = "OWO"

        gmi = GameMenuItems(self.game, None,
                            btn, "New Island",
                            des)
        gmi.cost = cost
        self.items.append(gmi)


class Dialog:
    def __init__(self, game):
        self.game = game
        self.bg = self.game.assets.images['ui/dialog.png']
        self.text = ""
        self.wrappedText = textWrap("", self.game.assets.font, self.bg.get_width() - 50)
        self.bgPos = colCenter(self.bg, bottom(self.bg, (0, 0))) - np.array((0, 200))
        self.on = False
        self.start = None
        self.end = None

        def temp():
            self.game.UIManager.dialogManager.next()
        self.func = temp

        self.fixColl()

    def fixColl(self):
        self.start = self.bgPos
        self.end = self.bgPos + np.array((self.bg.get_width(), self.bg.get_height()))

    def update(self):
        mp = pygame.mouse.get_pos()
        if mp[0] < self.end[0] and mp[0] > self.start[0] and mp[1] < self.end[1] and mp[1] > self.start[1]:
            self.func()
            return True

        return False

    def setText(self, text):
        self.text = text
        self.wrappedText = textWrap(text, self.game.assets.font, self.bg.get_width() - 50)

    def render(self, surf):
        if not self.on:
            return
        surf.blit(self.bg, self.bgPos)
        bgPos = self.bgPos + np.array((30, 25))

        for i, text in enumerate(self.wrappedText):
            textRender = self.game.assets.font.render(text, True, (200, 200, 200))
            surf.blit(textRender, bgPos + np.array((0, 20 * i)))
    def print(self, text):
        self.game.UITimer.timers.clear()
        self.setText(text)
    def say(self, text, delayTime):
        self.setText("")

        fullText = textWrap(text, self.game.assets.font, self.bg.get_width() - 50)
        count = 0

        for i, line in enumerate(fullText):
            for j, char in enumerate(line):
                self.game.UITimer.add(count * delayTime, lambda char=char: self.addChar(char))
                count += 1

            self.game.UITimer.add(count * delayTime, lambda: self.addChar(" "))
            count += 1


    def addChar(self, char):
        self.text += char
        self.wrappedText = textWrap(self.text, self.game.assets.font, self.bg.get_width() - 50)
