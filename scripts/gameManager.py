import random

from scripts.objects import *
from scripts.utils import *
import json
from scripts.tiles import *
from  scripts.timer import *
import time

class GameManager:

    def __init__(self, game):
        self.game = game

        self.zoomFactor = 3
        self.player_speed = 1

        self.viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camPos = np.array((0, 0), dtype=float)

        self.clock = pygame.time.Clock()

        self.tilemaps = {
            'main': StaticTilemap(
                Tileset(load_image("tileset/tileset.png"), size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH)),
            'object': StaticTilemap(
                Tileset(load_image("tileset/energy.png"), size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH))
        }
        self.now = 0
        self.player = Player(self.game.assets.images["player/idle"], tilePosToPos((14, 8)), self.game),
        self.particles = []
        self.objects = []
        self.tileObjects = []
        self.islands = [
        ]

        self.currentIsland = None
        self.currentIslandIndex = 0
        self.playerAtt = PlayerAtt()


        with open('resources/map/mineUpgrades.json', 'r') as file:
            data = json.load(file)
            self.mineUpgrades = data

        self.upgradeChances = {}

        chanceGen = 0
        for i in data:
            print(i)
            chanceGen += data[i]['chance']
            self.upgradeChances[i] = chanceGen
        self.maxChance = chanceGen

        with open('resources/map/player.json', 'r') as file:
            data = json.load(file)
            self.playerUpgrades = data

        #for mines
        self.combo = 0
        self.prvElement = -1

        #for actions, 0 : mine, 1 : move, 2 : upgrade
        self.action = 0

        self.water = 500
        self.fire = 500
        self.lightening = 100
        self.air = 500

        self.level = 0

    def newGame(self):

        # self.tilemaps['main'].loadFromCsv('map/firstIsland.csv')
        self.islands = [
            Island((0,0), "resources/map/4.csv", self.tilemaps["main"], self.game),
            # Island((0, 7), "resources/map/8.csv", self.tilemaps["main"], self.game)
            # getIslandFromJson('resources/map/basicIsland.json', self.game),
            # getIslandFromJson('resources/map/secondIsland.json', self.game)
        ]

        self.game.UIManager.dialogManager.setDialog("""튜토리얼 / 예상 소요시간 : 1 ~ 2분 / *터치*
        이 게임은 자원을 모아 채광기를 업그레이드 하고, 새로운 섬을 개척해 나가는 게임입니다.
        가운데 보이는 곡괭이 모양의 버튼은 현재 플레이어가 채집 상태임을 말합니다.
        이 상태에서는 화면의 좌우를 터치하여 자원을 채집할 수 있습니다.
        자원의 채집은 같은 색깔의 원소 타일 방향의 화면을 누르는 것으로 가능합니다.
        이제 가운데 보이는 곡괭이 모양의 버튼을 눌러보십시오.
        가운데 버튼이 신발 모양으로 바뀝니다.
        이 상태에서는 화면의 좌우를 터치하여 섬 또는 채집지 간의 이동이 가능합니다.
        현재 상태에서는 이동할 대상이 없어 이동이 불가할 겁니다.
        각각의 섬과 채집지는 각각의 특성을 가지고 있어, 이동 기능을 잘 사용하는 것이 중요합니다.
        다시 한번 가운데 버튼을 눌러보세요.
        이번에는 위에 화살표 모양이 보일겁니다.
        이 상태에서는 자동으로 업그레이드 메뉴가 뜨며, 화면의 좌우를 터치하여 메뉴를 전환할 수 있습니다.
        각각의 메뉴에서는 현재 플레이어가 있는 섬 또는 채집지에 대한 업그레이드가 가능합니다.
        화면 좌측 상단에 있는 사색의 숫자들이 플레이어가 가지고 있는 자원, 원소들의 양이며, 업그레이드에는 이 원소들이 소비됩니다.
        빨강, 파랑, 청록, 노랑 별로 불, 물, 공기, 전기 원소입니다.
        또한 New Island라는 제목을 가진 메뉴에서는 새로운 섬을 개척할 수 있습니다.
        새로운 섬을 개척하는 것이 이 게임의 궁극적인 목표이자, 이를 통해 플레이어는 더욱 많은 자원을 얻을 수 있습니다.
        처음으로 하는 섬 확장은 무료이니 지금 바로 섬을 확장해 보세요!
        한 번 더 가운데 위치한 버튼을 눌러보면 버튼이 다시 곡괭이 모양이 된 것을 볼 수 있습니다.
        곡괭이, 신발, 화살표 모양을 가진 버튼 세가지 상태가 플레이어의 기본 상태라 할 수 있겠습니다.
        이상으로 튜토리얼을 마치겠습니다.""")
        self.game.UIManager.dialogManager.next()

    def loadSave(self, saveFilePath):
        with open(saveFilePath, 'rb') as file:
            save = pickle.load(file)
        self.islands, self.fire, self.water, self.air, self.lightening, self.combo, self.prvElement,self.currentIslandIndex, self.level, self.playerAtt = save.islands, save.fire, save.water, save.air, save.lightening, save.combo, save.prvElement, save.currentIslandIndex, save.level, save.playerAtt

        for i in self.islands:
            for l in i.objects:
                l.load(self.game)
    def save(self):
        gameSave = GameSave(self.islands, self.fire, self.water,
                            self.air, self.lightening, self.combo, self.prvElement, self.currentIslandIndex, self.level, self.playerAtt)
        with open('save.pkl', 'wb') as file:
            pickle.dump(gameSave, file)

    def load(self):

        for i in self.islands:
            i.targetTilemap = self.tilemaps['main']
            i.load(self.game)
            for l in i.objects:
                l.targetTilemap = self.tilemaps['object']
                # l.load(self.game)

        self.currentIsland = self.islands[self.currentIslandIndex]

        self.game.gameManager.currentIsland.sync()
        targetObject = self.game.gameManager.currentIsland.currentObject
        self.game.gameManager.player[0].pos = np.array(
            tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[0], dtype=float)))

        for i in self.tileObjects:
            i.loadStructureFromCsv()
            i.placeOnTilemap()

        for i in self.islands:
            # i.loadStructureFromCsv()
            i.placeOnTilemap()
            for l in i.objects:
                l.placeOnTilemap()


    def run(self):
        self.load()
        prevTime = time.time()
        dragging = False
        lastUpdated = 0
        timeCounter = 0
        dt = 0

        pygame.mixer.music.load('resources/sound/bgm.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        while True:
            self.now = time.time()
            dt = self.now - prevTime
            prevTime = self.now
            timeCounter += dt

            self.game.timer.update()
            self.game.UITimer.update()
            self.game.bossTimer.update()

            self.game.eventHandler.update()

            self.game.renderer.render(dt)
            self.now += self.clock.tick(60)

    def act(self, *args):

        if self.action == 0:
            # print("okay")
            targetObject = self.game.gameManager.currentIsland.currentObject
            if type(targetObject) == TileMine:
                # print("then")
                if not targetObject.on:
                    # print("yay")
                    if not targetObject.working:
                        targetObject.working = True
                        targetObject.spawnTileObject(self.game)
                else:
                    targetObject.mine(args[0])
        elif self.action == 1:
            if args[0] == 0:
                if self.game.gameManager.currentIsland.currentObjectIndex > 0:

                    self.game.gameManager.currentIsland.currentObjectIndex -= 1
                    self.game.gameManager.currentIsland.sync()
                    targetObject = self.game.gameManager.currentIsland.currentObject
                    self.game.gameManager.player[0].pos = np.array(
                        tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[1], dtype=float)))
                elif self.game.gameManager.currentIslandIndex > 0:
                    self.game.gameManager.currentIslandIndex -= 1
                    self.game.gameManager.currentIsland = self.game.gameManager.islands[self.game.gameManager.currentIslandIndex]

                    targetObject = self.game.gameManager.currentIsland.currentObject
                    self.game.gameManager.player[0].pos = np.array(
                        tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[1], dtype=float)))
            elif args[0] == 1:
                if self.game.gameManager.currentIsland.currentObjectIndex < len(self.game.gameManager.currentIsland.objects)-1:
                    self.game.gameManager.currentIsland.currentObjectIndex += 1
                    self.game.gameManager.currentIsland.sync()
                    targetObject = self.game.gameManager.currentIsland.currentObject
                    self.game.gameManager.player[0].pos = np.array(
                        tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[0], dtype=float)))
                elif self.game.gameManager.currentIslandIndex < len(self.game.gameManager.islands) - 1:
                    self.game.gameManager.currentIslandIndex += 1
                    self.game.gameManager.currentIsland = self.game.gameManager.islands[self.game.gameManager.currentIslandIndex]

                    targetObject = self.game.gameManager.currentIsland.currentObject
                    self.game.gameManager.player[0].pos = np.array(
                        tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[1], dtype=float)))
        elif self.action == 2:
            if(args[0] == 1):
                self.game.UIManager.menuIndex += 1
                if self.game.UIManager.menuIndex > 2:
                    self.game.UIManager.menuIndex = 0
                # self.game.UIManager.menu = self.game.UIManager.menus[self.game.UIManager.menuIndex]
                self.updateMenu()

                # self.game.UIManager.menu.on = True
            else:
                self.game.UIManager.menuIndex -= 1
                if self.game.UIManager.menuIndex < 0:
                    self.game.UIManager.menuIndex = 2
                # self.game.UIManager.menu = self.game.UIManager.menus[self.game.UIManager.menuIndex]
                self.updateMenu()

    def mine(self, element):
        self.game.upgradeAdapter.calc()
        if self.prvElement == element:
            #calc added feature
            addedCombo = 1 # comboValue

            addedCombo += self.game.upgradeAdapter.add

            if element == 0:
                addedCombo += self.game.upgradeAdapter.fire
            if element == 1:
                addedCombo += self.game.upgradeAdapter.water
            if element == 2:
                addedCombo += self.game.upgradeAdapter.air

            if self.combo > 1000:
                addedCombo *= 4
            elif self.combo > 500:
                addedCombo *= 3
            elif self.combo > 100:
                addedCombo *= 2

            self.combo += addedCombo

        else:
            print(self.playerAtt.barrier, self.playerAtt.isBarrier)
            if not self.playerAtt.barrier:
                self.playerAtt.barrier = self.playerAtt.isBarrier

                if self.combo > 200:
                    self.game.assets.sounds['fail200'].play()
                else:
                    self.game.assets.sounds['fail50'].play()

                addEle = self.combo
                if self.prvElement == 0:
                    self.fire += addEle
                elif self.prvElement == 1:
                    self.water += addEle
                elif self.prvElement == 2:
                    self.air += addEle
                elif self.prvElement == 3:
                    self.lightening += addEle

                self.game.renderer.shakeScreen(min(self.combo / 10, 300))
                self.combo = 0

                self.prvElement = element

            self.playerWrong()

        if self.combo == 0:
            self.prvElement = element
            self.playerAtt.barrier = self.playerAtt.isBarrier

        return


    def changeAct(self, *args):
        self.game.assets.sounds['change'].play()
        self.action += 1
        if self.action == 2:
            self.updateMenu()
            self.game.UIManager.menu.on = True
        else:
            self.game.UIManager.menu.on = False
        if self.action > 2:
            self.action = 0
        # self.game.UIManager.menu.changeAct(self.action)



    # def updateFromRevolution(self, mine):
    #     self.title = "Revolution"
    #     self.items = [
    #
    #     ]
    #     temp = partial(self.temp, )
    #
    #     if len(data['costs']) - 1 > key:
    #         if self.game.gameManager.fire >= data['costs'][key][0] and self.game.gameManager.water >= \
    #                 data['costs'][key][1] and self.game.gameManager.air >= data['costs'][key][
    #             2] and self.game.gameManager.lightening >= data['costs'][key][3]:
    #             btn = ImageButton([self.game.assets['ui/smallBtn.png'], self.game.assets['ui/smallBtnPressed.png']],
    #                               (0, 0), temp)
    #         else:
    #             btn = ImageButton(
    #                 [self.game.assets['ui/smallBtnPressed.png'], self.game.assets['ui/smallBtnPressed.png']],
    #                 (0, 0), temp)
    #
    #     else:
    #         btn = 0
    #
    #     gmi = GameMenuItems(data['image'],
    #                         btn, data['title'],
    #                         data['descriptions'][key])
    #     gmi.cost = data['costs'][key]
    #     self.items.append(gmi)
    def playerAttaked(self, value):
        self.playerAtt.hp -= value
        self.player[0].hpBarAlpha = 2000

    def playerWrong(self):
        self.playerAtt.barrier = False
        #playsound

    def updateMenu(self):
        if self.game.UIManager.menuIndex == 0:
            self.game.UIManager.menu.updateFromMine(self.game.gameManager.currentIsland.currentObject)
        elif self.game.UIManager.menuIndex == 1:
            self.game.UIManager.menu.updateFromPlayer()
        elif self.game.UIManager.menuIndex == 2:
            self.game.UIManager.menu.updateFromNew(self.game.gameManager.currentIsland)

    def spawnNewIsland(self):
        # print(self.currentIsland.end)

        a = random.randint(-1, 3)
        b = 3 - a

        self.game.renderer.shakeScreen(100)
        self.game.renderer.targetPos = tilePosToPos(self.currentIsland.pos + np.array(self.currentIsland.end) + np.array((a + 3, b + 3)))
        self.game.renderer.camTarget = 1

        def temp():
            self.game.renderer.camTarget = 0

        self.game.timer.add(2000, temp)

        self.islands.append(
            Island(self.currentIsland.pos + np.array(self.currentIsland.end) + np.array((a, b)), "resources/map/" + str(random.randint(2, 8)) + ".csv", self.tilemaps['main'], self.game))

class PlayerAtt:
    def __init__(self):
        self.hp = 1
        self.maxHP = 1
        self.barrier = True
        self.isBarrier = True

        self.psychopath = False
        self.reviver = False
        self.attacker = False

        self.upgrades = {
            'hp': 1
        }

    def adaptUpgrade(self):
        if 'hp' in self.upgrades:
            self.maxHP = self.upgrades['hp']

        if 'reviver' in self.upgrades:
            self.reviver = self.upgrades['reviver']

        if 'psychopath' in self.upgrades:
            self.psychopath = self.upgrades['psychopath']

        if 'attacker' in self.upgrades:
            self.attacker = self.upgrades['attacker']


class GameSave:
    def __init__(self, islands, fire, water, air, lightening, combo, prvElement, currentIslandIndex, level, playerAtt):
        self.islands = islands
        self.fire = fire
        self.water = water
        self.air = air
        self.lightening = lightening
        self.combo = combo
        self.prvElement = prvElement
        self.currentIslandIndex = currentIslandIndex
        self.level = level
        self.playerAtt = playerAtt
