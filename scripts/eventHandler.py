import sys
from scripts.gameManager import *

class EventHandler:

    def __init__(self, game):
        self.game = game
        self.left = 0
        self.right = 0

        self.dragging = False
        self.dragStartPos = 0

        self.btnOns = []

    def update(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                a = self.game.UIManager.uiEvent()
                if a:
                    self.btnOns.append(a[1])
                    continue

                if self.game.UIManager.menu.on:
                    if pygame.mouse.get_pos()[1] < SCREEN_HEIGHT*0.7:
                        self.dragging = True
                        self.dragStartPos = pygame.mouse.get_pos()[1]
                        continue

                if pygame.mouse.get_pos()[0] <= SCREEN_WIDTH/2:
                    self.leftC()
                else:
                    self.rightC()
            elif event.type == pygame.MOUSEBUTTONUP:
                for i in self.btnOns:
                    i()
                self.up()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.gameManager.changeAct()
                if event.key == pygame.K_LEFT:
                    # self.game.gameManager.movement[0] = True
                    self.leftC()
                elif event.key == pygame.K_RIGHT:
                    # self.game.gameManager.movement[1] = True
                    self.rightC()
                elif event.key == pygame.K_UP:
                    self.game.gameManager.movement[2] = True
                    pass
                elif event.key == pygame.K_DOWN:
                    self.game.gameManager.movement[3] = True
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.up()
                if event.key == pygame.K_RIGHT:
                    self.up()
                if event.key == pygame.K_UP:
                    self.game.gameManager.movement[2] = False
                    pass
                if event.key == pygame.K_DOWN:
                    self.game.gameManager.movement[3] = False
                    pass
                if event.key == pygame.K_q:
                    self.game.gameManager.save()
                    # self.game.gameManager.islands.append(Island(
                    #
                    # ))
                    # self.game.currentIsland.currentObject = getRandomTileMine(game = self.game, pos = self.game.currentIsland.currentObject.pos)
                    pass
                    # self.game.currentIsland.objects[0].spawnTileObject(self.game)

                    # targetZoom += 0.5
                elif event.key == pygame.K_w:
                    pass

            if self.dragging:
                self.game.UIManager.targetScrollOffset = min(0, (pygame.mouse.get_pos()[1] - self.dragStartPos))

    def leftC(self):
        self.left = 1
        self.game.gameManager.act(0)
        # print(self.game.tileObjects[0].mine(0)[0])
    def up(self):
        self.dragging = False
        self.right, self.left = 0, 0

    def rightC(self):
        self.right = 1
        self.game.gameManager.act(1)
        # print(self.game.tileObjects[0].mine(1)[0])