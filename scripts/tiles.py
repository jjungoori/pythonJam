import pygame
import numpy as np
from constants import *
import csv

class Tileset:
    def __init__(self, file, zoomFactor, size=(16, 16), margin=0, spacing=0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file).convert_alpha() # Ensure the image has an alpha channel
        self.rect = self.image.get_rect()
        self.tiles = []
        self.tileImagePaths = []
        self.load(zoomFactor)

    def load(self, zoomFactor):
        self.tiles = []
        self.tileImagePaths = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.size, pygame.SRCALPHA) # Create a surface with an alpha channel
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                newSize = (int(tile.get_width() * zoomFactor), int(tile.get_height() * zoomFactor))
                upscaledTile = pygame.transform.scale(tile, newSize)
                self.tiles.append(upscaledTile)

                # tileImagePath = f'resources/structure/tile_image{x}_{y}.png'
                # pygame.image.save(tile, tileImagePath)

class StaticTilemap:
    def __init__(self, tileset, size=(10, 20)):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

    def loadFromCsv(self, csvFilePath):
        with open(csvFilePath, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, tileIndex in enumerate(row):
                    self.map[i, j] = int(tileIndex)

    def render(self, screen, viewport, chunkSize=(5, 5), zoomFactor=1):

        startChunkX = viewport.left // (chunkSize[0] * TILE_SIZE * zoomFactor)
        endChunkX = (viewport.right // (chunkSize[0] * TILE_SIZE * zoomFactor)) + 1
        startChunkY = viewport.top // (chunkSize[1] * TILE_SIZE * zoomFactor)
        endChunkY = (viewport.bottom // (chunkSize[1] * TILE_SIZE * zoomFactor)) + 1

        for chunkX in range(startChunkX, endChunkX):
            for chunkY in range(startChunkY, endChunkY):
                startX = chunkX * chunkSize[0]
                endX = startX + chunkSize[0]
                startY = chunkY * chunkSize[1]
                endY = startY + chunkSize[1]

                for i in range(startY, endY):
                    for j in range(startX, endX):
                        if self.map[i, j] <= 0:
                            continue

                        tile = self.tileset.tiles[self.map[i, j]]
                        screen.blit(tile, (
                        (j * TILE_SIZE * zoomFactor) - viewport.left, (i * TILE_SIZE * zoomFactor) - viewport.top))

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)


# class Tile(pygame.sprite.Sprite):
#     def __init__(self, image):
#         super().__init__()
#         self.image = image
#         self.rect = self.image.get_rect()
#
# # class DynamicTilemap:
#     def __init__(self, tileset, size=(10, 20)):
#         self.size = size
#         self.tileset = tileset
#         self.tilesGroup = pygame.sprite.Group()
#         self.map = np.zeros(size, dtype=object)
#         for i in range(size[0]):
#             for j in range(size[1]):
#                 tileImage = tileset.tiles[np.random.randint(len(tileset.tiles))]
#                 tile = Tile(tileImage)
#                 tile.rect.topleft = (i * TILE_SIZE, j * TILE_SIZE)
#                 self.map[i, j] = tile
#                 self.tilesGroup.add(tile)
#
#     def update(self, viewport):
#         for i in range(self.size[0]):
#             for j in range(self.size[1]):
#                 tile = self.map[i, j]
#                 tile.rect.topleft = ((i * TILE_SIZE) - viewport.left, (j * TILE_SIZE) - viewport.top)
#
#     def render(self, screen, viewport):
#         for tile in self.tilesGroup:
#             screen.blit(tile.image, (tile.rect.x - viewport.left, tile.rect.y - viewport.top))
#
#     def placeTile(self, i, j, tileIndex):
#         tileImage = self.tileset.tiles[tileIndex]
#         tile = Tile(tileImage)
#         tile.rect.topleft = (i * TILE_SIZE, j * TILE_SIZE)
#         self.map[i, j] = tile
#         self.tilesGroup.add(tile)