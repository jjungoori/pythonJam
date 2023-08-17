import pygame
import numpy as np
from scripts.constants import *
import csv


class GameObject(pygame.sprite.Sprite):
    def __init__(self, animation, position):
        pygame.sprite.Sprite.__init__(self)
        self.pos = np.array(position, dtype=float)

        self.animation = animation

    def update(self):
        self.animation.update()

    def render(self, screen, viewport):
        # objectScreen_x = int(game_object.pos[0] * zoomedTileSize - viewport.left)
        # objectScreen_y = int(game_object.pos[1] * zoomedTileSize - viewport.top)
        #
        # scaledImageWidth = int(game_object.image.get_width() * zoomFactor)
        # scaledImageHeight = int(game_object.image.get_height() * zoomFactor)
        # scaledImage = pygame.transform.scale(game_object.image, (scaledImageWidth, scaledImageHeight))

        screen.blit(self.animation.img(), self.pos-(viewport.top, viewport.left))

class TileObject:
    def __init__(self, pos, targetTilemap, csvStructure, size):
        self.pos = pos
        self.targetTilemap = targetTilemap
        self.csvStructure = csvStructure
        self.structure = np.zeros(size, dtype=int)
        self.loadStructureFromCsv()

    def loadStructureFromCsv(self):
        with open(self.csvStructure, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, tileIndex in enumerate(row):
                    self.structure[i, j] = int(tileIndex)

    def placeOnTilemap(self):
        print(self.structure.shape[0], self.structure.shape[1])
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
