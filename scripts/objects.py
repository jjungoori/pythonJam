import pygame
import numpy as np
from constants import *


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, position, images = []):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.pos = np.array(position, dtype=float)

        self.images = [*map(lambda x : pygame.image.load(x), images)]
        self.imageNum = 0

def updateObjects(object_list):

    for game_object in object_list:
        if game_object.images:
            game_object.imageNum += 1
            if game_object.imageNum >= len(game_object.images):
                game_object.imageNum = 0
            game_object.image = game_object.images[game_object.imageNum]


def render_objects(object_list, viewport, screen, zoomFactor):
    zoomedTileSize = TILE_SIZE * zoomFactor
    for game_object in object_list:

        object_screen_x = int(game_object.pos[0] * zoomedTileSize - viewport.left)
        object_screen_y = int(game_object.pos[1] * zoomedTileSize - viewport.top)

        scaledImageWidth = int(game_object.image.get_width() * zoomFactor)
        scaledImageHeight = int(game_object.image.get_height() * zoomFactor)
        scaledImage = pygame.transform.scale(game_object.image, (scaledImageWidth, scaledImageHeight))

        screen.blit(scaledImage, (object_screen_x, object_screen_y))

# class tileObject:
#     def __init__(self, struct, pos):
#         self.pos = pos
#         self.struct = struct
#
#     def render(self, tilemap, pos=None):
#         if pos != None:
#             self.pos = pos
#         for i in range(len(self.struct)):
#             for j in range(len(self.struct[i])):
#                 tilemap[self.pos[0] + i][self.pos[1] + j] = self.struct[i][j]
