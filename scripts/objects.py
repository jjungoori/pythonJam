import random
import json
from scripts.utils import *
from scripts.particle import *
import pickle



class GameObject(pygame.sprite.Sprite):
    def __init__(self, animation, position):
        pygame.sprite.Sprite.__init__(self)
        self.pos = np.array(position, dtype=float)

        self.animation = animation

    def update(self):
        self.animation.update()

    def center(self):
        return self.pos + (TILE_SIZE, TILE_SIZE)
    def render(self, screen, viewport):
        # objectScreen_x = int(game_object.pos[0] * zoomedTileSize - viewport.left)
        # objectScreen_y = int(game_object.pos[1] * zoomedTileSize - viewport.top)
        #
        # scaledImageWidth = int(game_object.image.get_width() * zoomFactor)
        # scaledImageHeight = int(game_object.image.get_height() * zoomFactor)
        # scaledImage = pygame.transform.scale(game_object.image, (scaledImageWidth, scaledImageHeight))

        objectScreenX = int(self.pos[0] - viewport.top)
        objectScreenY = int(self.pos[1] - viewport.left)
        screen.blit(self.animation.img(), (objectScreenX, objectScreenY))

class Player(GameObject):
    def __init__(self, animation, position):
        super().__init__(animation, position)
    def render(self, screen, viewport):
        screen.blit(self.animation.img(), self.pos - (viewport.top, viewport.left))


import csv
import numpy as np

class TileObject:
    def __init__(self, pos, targetTilemap, csvStructure):
        self.pos = pos
        self.targetTilemap = targetTilemap
        self.csvStructure = csvStructure
        self.structure = None
        self.on = True
        self.working = False

        self.run()

    def run(self):
        self.loadStructureFromCsv()

    def loadStructureFromCsv(self):
        rows = []
        with open(self.csvStructure, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append([int(tileIndex) for tileIndex in row])

        numRows = len(rows)
        numCols = len(rows[0]) if numRows > 0 else 0
        self.structure = np.zeros((numRows, numCols), dtype=int)

        for i in range(numRows):
            for j in range(numCols):
                self.structure[i, j] = rows[i][j]


    def placeOnTilemap(self):
        # print(self.structure.shape[0], self.structure.shape[1])
        if not self.on:
            return
        for i in range(self.structure.shape[0]):
            for j in range(self.structure.shape[1]):
                tileIndex = self.structure[i, j]
                if tileIndex != -1:
                    self.targetTilemap.map[i + self.pos[1], j + self.pos[0]] = tileIndex

    def changeTile(self, x, y, newTileIndex):
        if 0 <= x < self.structure.shape[1] and 0 <= y < self.structure.shape[0]:
            self.structure[y, x] = newTileIndex
            self.targetTilemap.map[y + self.pos[1], x + self.pos[0]] = newTileIndex
        else:
            print("Coordinates are out of bounds")


def getTileMine(jsonFile, pos, game):
    with open(jsonFile, 'r') as file:
        data = json.load(file)
        return TileMine(**data, targetTilemap=game.gameManager.tilemaps['object'], game = game, pos = pos)
   #
def getRandomTileMine(pos, game):
    upgradeVal = random.randint(0, game.gameManager.maxChance)
    upgrades = {}

    for i in game.gameManager.upgradeChances:
        if game.gameManager.upgradeChances[i] >= upgradeVal:
            upgrades[i] = 0

    a  = [0, 1, 2, 3]
    return TileMine(
        targetTilemap=game.gameManager.tilemaps['object'], game = game, pos = pos, csvStructure="resources/map/tilemine.csv",
        elements=(a.pop(random.randint(0,3)), a.pop(random.randint(0,2))),
        upgrades=upgrades
    )

class TileMine(TileObject):

    def __init__(self, pos, targetTilemap, csvStructure, game, upgrades, elements):
        print("tilemineSpwan")
        super().__init__(pos, targetTilemap, csvStructure)
        self.tileMatch = {
            1 : [[48, 70, 92], [115, 137, 159]],
            0 : [[114, 136, 158], [49, 71, 93]],
            3 : [[50, 72, 94], [117, 139, 161]],
            2 : [[116, 138, 160], [51, 73, 95]]
        }
        self.on = False
        self.upgrades = upgrades
        self.elements = elements
        self.tiles = np.array([self.elements, self.elements, self.elements])
        self.game = game
        self.playerOffsetPos = ((-0.25,2), (1.25,2))
        self.prvElement = -1
        self.readyObject = 0

        # self.load(game)
        print("tilemineSpawned")
        # self.sync()

    def __getstate__(self):
        state = self.__dict__.copy()

        delState = ['game', 'readyObject', 'targetTilemap']
        for i in delState:
            if i in state:
                del state[i]

        return state

    def load(self, game):
        self.game = game
        # self.working = False
        # self.on = False
        if self.on == False:
            self.readyObject = GameObject(Animation(load_images('entity/spawner'), loop=False, img_dur=4, start=False),
                                          tilePosToPos(self.pos))
            self.readyObject.pos[1] -= 16
            self.game.gameManager.objects.append(self.readyObject)


    def spawnTileObject(self, game):
        game.assets.sounds['mineSpawnStart'].play()
        # print(tilePosToPos(self.pos))
        self.readyObject.animation.start = True
        def temp():
            game.assets.sounds['mineSpawn'].play()
            game.renderer.shake = 30
            game.gameManager.objects.remove(self.readyObject)
            for i in range(100):
                game.gameManager.particles.append(
                    Particle(tilePosToPos(self.pos+np.array((1,0.5+3.5/100*i),int)), ((random.random() - 0.5) * 20, (random.random() - 0.5) * 20), 5.0,
                             random.random() + 0.01,
                             (random.random() * 255, random.random() * 255, random.random() * 255), 0, 0))
            self.on = True
            self.sync()
        game.timer.add(self.readyObject.animation.img_duration*len(self.readyObject.animation.images)*10+2000, temp)


    def sync(self):
        # print(self.tiles)
        for i in range(3):
            self.structure[i][0] = self.tileMatch[self.tiles[i][0]][0][i]
            self.structure[i][1] = self.tileMatch[self.tiles[i][1]][1][i]
        self.placeOnTilemap()
    def mine(self, lr):
        self.game.assets.sounds['mine'].play()
        # print(tilePosToPos(self.pos + np.array(self.playerOffsetPos[lr])), self.game.gameManager.player[0].pos)
        self.game.gameManager.player[0].pos = np.array(tilePosToPos(self.pos + np.array(self.playerOffsetPos[lr], dtype=float)))
        getTiles = (self.tiles[2][0], self.tiles[2][1])
        self.tiles[2] = self.tiles[1]
        self.tiles[1] = self.tiles[0]
        l = random.randint(0,1)
        if l == 0:
            r = self.elements[0]
            l = self.elements[1]
        else:
            r = self.elements[1]
            l = self.elements[0]
        self.tiles[0] = np.array([l, r], dtype=int)

        self.sync()
        self.game.renderer.shakeScreen(0.2)
        self.game.gameManager.mine(getTiles[lr])
        return getTiles[lr]

    def upgrade(self, *args):
        if args[0] not in self.upgrades:
            self.upgrades[args[0]] = 0
        self.upgrades[args[0]] += 1
        return

    def save(self):
        with open('testMineSave.pkl', 'wb') as file:
            pickle.dump(self, file)

def getIslandFromJson(jsonFile, game):
    with open(jsonFile, 'r') as file:
        data = json.load(file)
        print('json imported')
        return Island(**data, targetTilemap=game.gameManager.tilemaps['main'], game=game)

def getNewIslandFromJson(jsonFile, game): # don't care the tilemines
    with open(jsonFile, 'r') as file:
        data = json.load(file)
        print('json imported')
        island =  Island(**data, targetTilemap=game.gameManager.tilemaps['main'], game=game)
        island.resetObjects()

def getIslandFromPickle(pickleAdress):
    with open(pickleAdress, 'rb') as file:
        island = pickle.load(file)
    return island

class Island(TileObject):
    def __init__(self, pos, csvStructure, targetTilemap, objs, level, type, start, end, upgrades, game):
        self.objects = objs
        self.game = game

        super().__init__(pos, targetTilemap, csvStructure)
        self.type = 'whiteLand'
        self.level = level
        self.start = start
        self.end = end
        self.currentObjectIndex = 0
        self.upgrades = upgrades
        self.type = type

    def load(self, game):
        self.game = game
        self.currentObject = self.objects[self.currentObjectIndex]

    def resetObjects(self):
        for i in range(len(self.objects)):
            self.objects[i] = getRandomTileMine(self.objects[i].pos, self.game)

    def sync(self):
        self.currentObject = self.objects[self.currentObjectIndex]
    def run(self):
        # print("B")
        self.objects = getObjectsFromDict(self.objects, self.game, self.pos)
        # self.loadStructureFromCsv()
        # self.placeOnTilemap()

    def upgrade(self, *args):
        # print(args[0])
        if args[0] not in self.upgrades:
            self.upgrades[args[0]] = 0
        self.upgrades[args[0]] += 1
        return

    def __getstate__(self):
        state = self.__dict__.copy()
        delState = ['game', 'currentObject', 'targetTilemap']
        for i in delState:
            if i in state:
                del state[i]
        return state

    def save(self):
        with open('testSave.pkl', 'wb') as file:
            pickle.dump(self, file)

    # def load


def getObjectsFromDict(objsDict, game, pos):
    objs = []
    for i in objsDict:
        # print(i)
        if i == "tilemines":
            for l in objsDict[i]:
                # print(l)
                temp = getTileMine(l[0], pos + np.array(l[1]), game=game)
                # temp = getRandomTileMine(pos + np.array(l[1]), game = game)
                objs.append(temp)
    print(objs)
    return objs