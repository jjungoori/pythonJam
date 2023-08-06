import pygame
import sys
import numpy as np

# Game settings
TILE_SIZE = 32
WORLD_WIDTH = 100
WORLD_HEIGHT = 100

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Pygame initialization
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

object_image = pygame.image.load("cat.png")  # Ensure "object.png" exists
object_pos = np.array([WORLD_WIDTH // 2 + 5, WORLD_HEIGHT // 2 + 5], dtype=float)  # Position in world coordinates


# Tileset and Tilemap classes
class Tileset:
    def __init__(self, file, size=(32, 32), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)


class Tilemap:
    def __init__(self, tileset, size=(10, 20)):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

    def render(self, viewport):
        start_x = max(0, viewport.left // TILE_SIZE)
        end_x = min(self.size[0], start_x + viewport.width // TILE_SIZE + 2)
        start_y = max(0, viewport.top // TILE_SIZE)
        end_y = min(self.size[1], start_y + viewport.height // TILE_SIZE + 2)
        for i in range(start_y, end_y):
            for j in range(start_x, end_x):
                tile = self.tileset.tiles[self.map[i, j]]
                screen.blit(tile, ((j * TILE_SIZE) - viewport.left, (i * TILE_SIZE) - viewport.top))

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)


# Tileset and tilemap creation
tileset = Tileset("tileset.png", size=(TILE_SIZE, TILE_SIZE))  # Ensure "tileset.png" exists
tilemap = Tilemap(tileset, size=(WORLD_HEIGHT, WORLD_WIDTH))
tilemap.set_random()

player_pos = np.array([WORLD_WIDTH // 2, WORLD_HEIGHT // 2], dtype=float)
player_speed = 1
cam_pos = np.array([WORLD_WIDTH // 2, WORLD_HEIGHT // 2], dtype=float)  # Initialize camera position
cam_lerp_speed = 0.02  # Speed of camera lerp, tune this to your liking


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_pos[0] = max(0, player_pos[0] - player_speed)
            elif event.key == pygame.K_RIGHT:
                player_pos[0] = min(WORLD_WIDTH - 1, player_pos[0] + player_speed)
            elif event.key == pygame.K_UP:
                player_pos[1] = max(0, player_pos[1] - player_speed)
            elif event.key == pygame.K_DOWN:
                player_pos[1] = min(WORLD_HEIGHT - 1, player_pos[1] + player_speed)
    # Update camera position towards player with lerp
    cam_pos = (1 - cam_lerp_speed) * cam_pos + cam_lerp_speed * player_pos

    # Calculate the viewport rectangle
    viewport_x = int(cam_pos[0] * TILE_SIZE - SCREEN_WIDTH / 2 + TILE_SIZE / 2)
    viewport_y = int(cam_pos[1] * TILE_SIZE - SCREEN_HEIGHT / 2 + TILE_SIZE / 2)
    viewport = pygame.Rect(viewport_x, viewport_y, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Draw everything
    screen.fill((255, 255, 255))  # Clear screen
    tilemap.render(viewport)  # Draw tilemap

    # Draw object on the map
    object_screen_x = int((object_pos[0] * TILE_SIZE) - viewport.left)
    object_screen_y = int((object_pos[1] * TILE_SIZE) - viewport.top)
    screen.blit(object_image, (object_screen_x, object_screen_y))  # Draw object image at its screen position

    # Draw player in the center of the screen
    player_screen_x = int((player_pos[0] * TILE_SIZE - cam_pos[0] * TILE_SIZE) + SCREEN_WIDTH / 2)
    player_screen_y = int((player_pos[1] * TILE_SIZE - cam_pos[1] * TILE_SIZE) + SCREEN_HEIGHT / 2)
    pygame.draw.circle(screen, (0, 0, 255), (player_screen_x, player_screen_y), TILE_SIZE // 2)  # Draw player

    # Update screen
    pygame.display.flip()