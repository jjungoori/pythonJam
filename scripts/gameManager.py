import  pygame
from scripts.objects import *
import  numpy as np
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

        self.viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Define viewport here
        self.camPos = np.array((0, 0), dtype=float)

        self.clock = pygame.time.Clock()
        self.movement = [False, False, False, False]

        self.tilemaps = {
            'main': StaticTilemap(
                Tileset(load_image("tileset/tileset.png"), size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH)),
            'object': StaticTilemap(
                Tileset(load_image("tileset/energy.png"), size=(TILE_SIZE, TILE_SIZE)),
                size=(WORLD_HEIGHT, WORLD_WIDTH))
        }
        self.now = 0
        self.player = Player(self.game.assets.images["player/idle"], tilePosToPos((14, 8))),
        self.particles = []
        self.objects = []
        self.tileObjects = []
        self.islands = [
        ]

        self.currentIslandIndex = 0


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

        # self.game.UIManager.menus = [
        #     Menu(self.game, [
        #         MenuItems(None,
        #                   ImageButton([game.assets['ui/smallBtn.png'], game.assets['ui/smallBtnPressed.png']],
        #                               (0, 0), self.game.gameManager.currentIsland.upgrade, 'add'), 'island', 'add 1 combo per click'),
        #     ]),
            # Menu(self.game, [
            #     MenuItems(None,
            #               ImageButton([game.assets['ui/smallBtn.png'], game.assets['ui/smallBtnPressed.png']],
            #                           (0, 0), self.game.gameManager.currentIsland.currentObject.upgrade, 'add'), 'mine',
            #               'add 2 combo per click'),
            # ]),
            # Menu(self.game, [
            #     MenuItems(None,
            #               ImageButton([game.assets['ui/smallBtn.png'], game.assets['ui/smallBtnPressed.png']],
            #                           (0, 0), self.game.gameManager.currentIsland.currentObject.upgrade, 'add'), 'new',
            #               'add 1 combo per click'),
            # ]),
        # ]

        #for mines
        self.combo = 0
        self.prvElement = -1

        #for actions, 0 : mine, 1 : move, 2 : upgrade
        self.action = 0

        self.water = 0
        self.fire = 0
        self.lightening = 0
        self.air = 0


    def load(self):
        # self.tilemaps['main'].loadFromCsv('map/firstIsland.csv')
        self.islands = [
            getIsland('resources/map/basicIsland.json', self.game),
            getIsland('resources/map/secondIsland.json', self.game)
        ]
        self.currentIsland = self.islands[0]

        for i in self.tileObjects:
            i.loadStructureFromCsv()
            i.placeOnTilemap()

        for i in self.islands:
            i.loadStructureFromCsv()
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
            # Update logic here

            self.game.eventHandler.update()

            if self.movement[0]:
                self.player[0].pos[0] -= 1
            if self.movement[1]:
                self.player[0].pos[0] += 1
            if self.movement[2]:
                self.player[0].pos[1] -= 1
            if self.movement[3]:
                self.player[0].pos[1] += 1


            self.game.renderer.render(dt)
            self.now += self.clock.tick(60)

    def act(self, *args):

        if self.action == 0:
            targetObject = self.game.gameManager.currentIsland.currentObject
            if type(targetObject) == TileMine:
                if not targetObject.on:
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
                if self.game.UIManager.menuIndex == 0:
                    self.game.UIManager.menu.updateFromMine(self.game.gameManager.currentIsland.currentObject)
                elif self.game.UIManager.menuIndex == 1:
                    self.game.UIManager.menu.updateFromIsland(self.game.gameManager.currentIsland)

                self.game.UIManager.menu.on = True
            else:
                self.game.UIManager.menu.on = False

    def mine(self, element):
        if self.prvElement == element:
            #calc added feature
            addedCombo = 1000
            if 'add' in self.game.gameManager.currentIsland.currentObject.upgrades:
                addedCombo += self.mineUpgrades['add']['values'][self.game.gameManager.currentIsland.currentObject.upgrades['add']]

            if element == 0 and 'fireAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
                addedCombo += self.mineUpgrades['fireAdd']['values'][self.game.gameManager.currentIsland.currentObject.upgrades['fireAdd']]
            if element == 1 and 'waterAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
                addedCombo += self.mineUpgrades['waterAdd']['values'][self.game.gameManager.currentIsland.currentObject.upgrades['waterAdd']]
            if element == 2 and 'airAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
                addedCombo += self.mineUpgrades['airAdd']['values'][self.game.gameManager.currentIsland.currentObject.upgrades['airAdd']]


            self.combo += addedCombo
        else:
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

            self.game.renderer.shake = min(self.combo/10, 300)
            self.combo = 0
        self.prvElement = element
        return


    def changeAct(self, *args):
        self.game.assets.sounds['change'].play()
        self.action += 1
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

