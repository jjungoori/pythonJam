

import  pygame

GLOW_CACHE = {}

def glow_img(size, color):
    if (size, color) not in GLOW_CACHE:
        surf = pygame.Surface((size * 2 + 2, size * 2 + 2))
        pygame.draw.circle(surf, color, (surf.get_width() // 2, surf.get_height() // 2), size)
        surf.set_colorkey((0, 0, 0))
        GLOW_CACHE[(size, color)] = surf
    return GLOW_CACHE[(size, color)]

class Particle:
    def __init__(self, position, velocity, size, decay, color, physics, gravity, dead=False):
        self.position = list(position)
        self.velocity = list(velocity)
        self.size = size
        self.decay = decay
        self.color = color
        self.physics = physics
        self.gravity = gravity
        self.dead = dead

    def update(self, tiles=0, TILE_SIZE=0):
        if not self.dead and self.gravity:
            self.velocity[1] = min(self.velocity[1] + self.gravity, 3)
        else:
            self.velocity[0] *= 0.9
            self.velocity[1] *= 0.9


        self.position[0] += self.velocity[0]
        # if self.physics:
        #     if ((int(self.position[0] // TILE_SIZE), int(self.position[1] // TILE_SIZE)) in tiles) or (self.position[0] < TILE_SIZE) or (self.position[0] > DISPLAY_SIZE[0] - TILE_SIZE):
        #         self.position[0] -= self.velocity[0]
        #         self.velocity[0] *= -0.7

        self.position[1] += self.velocity[1]
        # if self.physics:
        #     if (int(self.position[0] // TILE_SIZE), int(self.position[1] // TILE_SIZE)) in tiles:
        #         self.position[1] -= self.velocity[1]
        #         self.velocity[1] *= -0.7
        #         if abs(self.velocity[1]) < 0.1:
        #             self.velocity[1] = 0
        #             self.dead = True

        self.size -= self.decay
        if self.size <= 1:
            return False

        return True

    def render(self, display, viewport, height, BLEND_RGBA_ADD):
        display.blit(glow_img(int(self.size * 1.5 + 2), (int(self.color[0] / 2), int(self.color[1] / 2), int(self.color[2] / 2))), (self.position[0] - self.size * 2 - viewport.top, self.position[1] + height - self.size * 2 - viewport.left), special_flags=BLEND_RGBA_ADD)
        display.blit(glow_img(int(self.size), self.color), (self.position[0] - self.size - viewport.top, self.position[1] + height - self.size - viewport.left), special_flags=BLEND_RGBA_ADD)
        display.set_at((int(self.position[0]) - viewport.top, int(self.position[1] + height)- viewport.left), (255, 255, 255))
