import random

import pygame
import numpy as np
from scripts.constants import *
from scripts.utils import *
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

        objectScreenX = int(self.pos[0] - viewport.left)
        objectScreenY = int(self.pos[1] - viewport.top)
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
        self.on = False


    def loadStructureFromCsv(self):
        with open(self.csvStructure, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, tileIndex in enumerate(row):
                    self.structure[i, j] = int(tileIndex)

    def placeOnTilemap(self):
        # print(self.structure.shape[0], self.structure.shape[1])
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

    def __init__(self, pos, targetTilemap, csvStructure):
        super().__init__(pos, targetTilemap, csvStructure, (3,2))

        self.tileMatch = {
            1 : [[48, 70, 92], [115, 137, 159]],
            0 : [[114, 136, 158], [49, 71, 93]]
        }
        self.tiles = np.array([[1,0],[1,0],[0,0]])
        # self.sync()

    def spawnTileObject(self, l):
        l.append(GameObject(Animation(load_images('entity/spawner'), loop=True, img_dur=8), tilePosToPos((14,8))))

    def sync(self):
        print(self.tiles)
        for i in range(3):
            self.structure[i][0] = self.tileMatch[self.tiles[i][0]][0][i]
            self.structure[i][1] = self.tileMatch[self.tiles[i][1]][1][i]
        self.placeOnTilemap()
    def mine(self):
        self.tiles[2] = self.tiles[1]
        self.tiles[1] = self.tiles[0]
        l = random.randint(0,1)
        if l == 0:
            r = 1
        else:
            r = 0
        self.tiles[0] = np.array([l, r], dtype=int)

        self.sync()

