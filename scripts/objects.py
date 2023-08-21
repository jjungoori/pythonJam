import random

import pygame
import numpy as np
from scripts.constants import *
from scripts.utils import *
from scripts.particle import *
import csv



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


class TileObject:
    def __init__(self, pos, targetTilemap, csvStructure, size):
        self.pos = pos
        self.targetTilemap = targetTilemap
        self.csvStructure = csvStructure
        self.structure = np.zeros(size, dtype=int)
        self.loadStructureFromCsv()
        self.on = True


    def loadStructureFromCsv(self):
        with open(self.csvStructure, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, tileIndex in enumerate(row):
                    self.structure[i, j] = int(tileIndex)

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

class TileMine(TileObject):

    def __init__(self, pos, targetTilemap, csvStructure, game):
        super().__init__(pos, targetTilemap, csvStructure, (3,2))
        self.tileMatch = {
            1 : [[48, 70, 92], [115, 137, 159]],
            0 : [[114, 136, 158], [49, 71, 93]]
        }
        self.tiles = np.array([[1,0],[1,0],[1,0]])
        self.on = False
        self.readyObject = GameObject(Animation(load_images('entity/spawner'), loop=False, img_dur=8, start = False), tilePosToPos(self.pos))
        self.readyObject.pos[1] -= 16
        self.game = game
        self.game.objects.append(self.readyObject)
        self.playerOffsetPos = ((-0.25,2), (1.25,2))
        # self.sync()

    def spawnTileObject(self, game):
        print(tilePosToPos(self.pos))
        self.readyObject.animation.start = True
        def temp():
            game.renderer.shake = 10
            game.objects.remove(self.readyObject)
            for i in range(100):
                game.particles.append(
                    Particle(tilePosToPos(self.pos+np.array((1,0.5+3.5/100*i),int)), ((random.random() - 0.5) * 20, (random.random() - 0.5) * 20), 5.0,
                             random.random() + 0.01,
                             (random.random() * 255, random.random() * 255, random.random() * 255), 0, 0))
            self.on = True
            self.sync()
        game.timer.add(self.readyObject.animation.img_duration*len(self.readyObject.animation.images)*10+2000, temp)


    def sync(self):
        print(self.tiles)
        for i in range(3):
            self.structure[i][0] = self.tileMatch[self.tiles[i][0]][0][i]
            self.structure[i][1] = self.tileMatch[self.tiles[i][1]][1][i]
        self.placeOnTilemap()
    def mine(self, lr):
        print(tilePosToPos(self.pos + np.array(self.playerOffsetPos[lr])), self.game.player[0].pos)
        self.game.player[0].pos = np.array(tilePosToPos(self.pos + np.array(self.playerOffsetPos[lr], dtype=float)))
        getTiles = (self.tiles[2][0], self.tiles[2][1])
        self.tiles[2] = self.tiles[1]
        self.tiles[1] = self.tiles[0]
        l = random.randint(0,1)
        if l == 0:
            r = 1
        else:
            r = 0
        self.tiles[0] = np.array([l, r], dtype=int)

        self.sync()
        self.game.renderer.shake = 0.3
        return getTiles[lr], 1

class Island:
    def __init__(self):
        self.tileMines = []
        self.type = 'whiteLand'
        self.level = 0