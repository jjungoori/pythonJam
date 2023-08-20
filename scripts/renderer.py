import pygame
from scripts.constants import *

class Renderer:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Elemental Sky')
        self.targetZoom = 3
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def render(self, game, dt):
        self.screen.fill((0, 0, 0, 0))
        self.display.fill((0, 0, 0, 0))

        for i in game.objects:
            i.update()
            i.render(self.display, game.viewport)
        for i in game.tilemaps:
            game.tilemaps[i].render(self.display,
                                    game.viewport)
        self.screen.blit(self.display, (0, 0))
        # zoomRect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        #
        # # Capture the area you want to zoom
        # capturedArea = self.screen.subsurface(zoomRect)
        #
        # # Scale the captured area based on the zoom factor
        # zoomedArea = pygame.transform.scale(capturedArea, (
        # int(zoomRect.width * self.zoomFactor), int(zoomRect.height * self.zoomFactor)))
        #
        # # Blit the zoomed area back to the screen at the desired position
        # self.screen.blit(zoomedArea, (zoomRect.left, zoomRect.top))

        game.zoomFactor = (1 - CAM_LERP_SPEED * dt) * game.zoomFactor + CAM_LERP_SPEED * dt * self.targetZoom
        game.camPos = (1 - CAM_LERP_SPEED * dt) * game.camPos + CAM_LERP_SPEED * dt * game.player[0].pos

        game.viewport.left = game.camPos[1] - (SCREEN_HEIGHT / game.zoomFactor) / 2 + TILE_SIZE / 2
        game.viewport.top = game.camPos[0] - (SCREEN_WIDTH / game.zoomFactor) / 2 + TILE_SIZE / 2
        # self.viewport.width = SCREEN_WIDTH / self.zoomFactor
        # self.viewport.height = SCREEN_HEIGHT / self.zoomFactor


        for i in game.tilemaps:
            game.tilemaps[i].render(self.display, game.viewport)
        for i in game.objects:
            i.update()
            i.render(self.display, game.viewport)
        for i in game.particles:
            if i.update():
                i.render(self.display, game.viewport, 1, 1)
            else:
                game.particles.remove(i)

        game.player[0].update()
        game.player[0].render(self.display, game.viewport)

        capturedContent = self.display.copy()

        zoomedContent = pygame.transform.scale(capturedContent, (
            int(SCREEN_WIDTH * game.zoomFactor), int(SCREEN_HEIGHT * game.zoomFactor)))
        game.ui.update(dt)
        game.ui.draw_ui(zoomedContent)

        self.screen.blit(zoomedContent, (0, 0))
        # self.screen.blit(self.display, (0,0))
        pygame.display.update()
