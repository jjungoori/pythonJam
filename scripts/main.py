import pygame
import sys
import numpy as np
import time
from tiles import *
from objects import *
from constants import *

zoomFactor = 1

player_speed = 1

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = GameObject("resources/entity/player/player1.png", [5, 5], [
    "resources/entity/player/player1.png",
    "resources/entity/player/player2.png"
])

# object2 = GameObject("dog.png", [WORLD_WIDTH // 3, WORLD_HEIGHT // 3])

objectList = [player]

tileset = Tileset("resources/tileset/tileset.png", zoomFactor, size=(TILE_SIZE, TILE_SIZE))
cloudTileset = Tileset("resources/tileset/cloud.png", zoomFactor, size=(TILE_SIZE, TILE_SIZE))
energyTileset = Tileset("resources/tileset/energy.png", zoomFactor, size=(TILE_SIZE, TILE_SIZE))

tilemap = StaticTilemap(tileset, size=(WORLD_HEIGHT, WORLD_WIDTH))
cloudTilemap = StaticTilemap(cloudTileset, size=(WORLD_HEIGHT, WORLD_WIDTH))
energyTilemap = StaticTilemap(energyTileset, size=(WORLD_HEIGHT, WORLD_WIDTH))

# dynamicTilemap = DynamicTilemap(tileset, )
tilemap.loadFromCsv("resources/map/firstIsland.csv")
# energyTilemap.loadFromCsv("resources/map/csv.csv")

# player.pos = np.array([WORLD_WIDTH // 2, WORLD_HEIGHT // 2], dtype=float)
camPos = player.pos

prevTime = time.time()

dragging = False
tileIndexToPlace = 1

lastUpdated = 0
timeCounter = 0

tilemine = TileObject((14,8), energyTilemap, 'resources/map/tilemine.csv', (3, 2))
tilemine.placeOnTilemap()

# for i in range(20):
#     objectList.append(GameObject(energyTileset.tiles[60+i].image, (5+i,5)))
# Game loop
pygame.transform.rotozoom(screen, 0, 20)

while True:
    now = time.time()
    dt = now - prevTime
    prevTime = now

    timeCounter += dt

    zoomedTileSize = TILE_SIZE * zoomFactor

    if timeCounter - lastUpdated >= 0.5:
        updateObjects(objectList)
        lastUpdated = timeCounter

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.pos[0] = max(0, player.pos[0] - player_speed)
            elif event.key == pygame.K_RIGHT:
                player.pos[0] = min(WORLD_WIDTH - 1, player.pos[0] + player_speed)
            elif event.key == pygame.K_UP:
                player.pos[1] = max(0, player.pos[1] - player_speed)
            elif event.key == pygame.K_DOWN:
                player.pos[1] = min(WORLD_HEIGHT - 1, player.pos[1] + player_speed)
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     dragging = True
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     dragging = False
            # elif event.type == pygame.MOUSEMOTION and dragging:
            #     x, y = event.pos
            #     i = (x + viewport.left) // TILE_SIZE
            #     j = (y + viewport.top) // TILE_SIZE
            #     dynamicTilemap.placeTile(i, j, tileIndexToPlace)


    #render
    camPos = (1 - CAM_LERP_SPEED * dt) * camPos + CAM_LERP_SPEED * dt * player.pos

    viewport_x = int(camPos[0] * zoomedTileSize - SCREEN_WIDTH / 2 + zoomedTileSize / 2)
    viewport_y = int(camPos[1] * zoomedTileSize - SCREEN_HEIGHT / 2 + zoomedTileSize / 2)
    viewportWidth = int(SCREEN_WIDTH)
    viewportHeight = int(SCREEN_HEIGHT)
    viewport = pygame.Rect(viewport_x, viewport_y, viewportWidth, viewportHeight)

    screen.fill((201, 225, 229))
    tilemap.render(viewport, screen, zoomFactor)
    energyTilemap.render(viewport, screen, zoomFactor)


    # dynamicTilemap.update(viewport)
    # dynamicTilemap.render(screen, viewport)

    renderObjects(objectList, viewport, screen, zoomFactor)

    # player_screen_x = int((player.pos[0] * zoomedTileSize - camPos[0] * zoomedTileSize) + SCREEN_WIDTH / 2)
    # player_screen_y = int((player.pos[1] * zoomedTileSize - camPos[1] * zoomedTileSize) + SCREEN_HEIGHT / 2)
    # pygame.draw.circle(screen, (0, 0, 255), (player_screen_x, player_screen_y), zoomedTileSize // 2)

    pygame.display.flip()

