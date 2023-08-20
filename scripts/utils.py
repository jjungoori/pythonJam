import os
import csv
import pygame
from scripts.constants import BASE_IMG_PATH, TILE_SIZE


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def tilePosToPos(pos):
    return (pos[0]*TILE_SIZE, pos[1]*TILE_SIZE)

class Animation:
    def __init__(self, images, img_dur=5, loop=True, start=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
        self.start = start

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if not self.start or self.done:
            return
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
                print("done")

    def img(self):
        return self.images[int(self.frame / self.img_duration)]