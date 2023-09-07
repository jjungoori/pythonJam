import os
import pygame
import random
from scripts.constants import *


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

def center(img, pos = (0,0)):
    return ((SCREEN_WIDTH - img.get_width())/2, (SCREEN_HEIGHT - img.get_height())/2)

def colCenter(img, pos = (0,0)):
    return ((SCREEN_WIDTH - img.get_width())/2, pos[1])

def rowCenter(img, pos = (0,0)):
    return (pos[0], (SCREEN_HEIGHT - img.get_height())/2)

def bottom(img, pos):
    return (pos[0], (SCREEN_HEIGHT-img.get_height()))

def textWrap(text, font, maxWidth):
    words = text.split(' ')
    lines = []
    line = []
    lineWidth = 0
    blankWidth = font.size(' ')[0]

    for word in words:

        wordWidth, temp = font.size(word)

        if lineWidth + wordWidth + blankWidth > maxWidth:
            lines.append(' '.join(line))
            line = []
            lineWidth = 0

        line.append(word)
        lineWidth += wordWidth + blankWidth

    lines.append(' '.join(line))
    return lines

def lvTo6(level):
    y = 1 + (level/3)
    if y > 6:
        y = 6
    return int(y)


def lvToRare(level, MAX):
    r = random.randint(0, MAX)
    w = level / 100.0

    wr = int((r * w) + r)

    if wr > MAX:
        wr = MAX

    return wr


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
                # print("done")


    def img(self):
        return self.images[int(self.frame / self.img_duration)]
