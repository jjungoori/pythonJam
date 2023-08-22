import  pygame
import  numpy as np
from scripts.utils import *

class GameManager:

    def __init__(self, game):
        self.game = game

        #for mines
        self.combo = 0
        self.prvElement = -1

        #for actions, 0 : mine, 1 : move, 2 : upgrade
        self.action = 0

        self.water = 0
        self.fire = 0
        self.lightening = 0
        self.air = 0

    def act(self, *args):

        if self.action == 0:
            targetObject = self.game.currentIsland.objects[self.game.currentIsland.currentObject]
            if not targetObject.on:
                targetObject.spawnTileObject(self.game)
            else:
                targetObject.mine(args[0])
        elif self.action == 1:
            if args[0] == 0 and self.game.currentIsland.currentObject > 0:
                self.game.currentIsland.currentObject -= 1
                targetObject = self.game.currentIsland.objects[self.game.currentIsland.currentObject]
                self.game.player[0].pos = np.array(
                    tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[1], dtype=float)))

            elif args[0] == 1 and self.game.currentIsland.currentObject < len(self.game.currentIsland.objects)-1:
                self.game.currentIsland.currentObject += 1
                targetObject = self.game.currentIsland.objects[self.game.currentIsland.currentObject]
                self.game.player[0].pos = np.array(
                    tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[0], dtype=float)))

    def mine(self, element):
        if self.prvElement == element:
            self.combo += 1
        else:
            if self.combo > 200:
                self.game.soundAssets['fail200'].play()
            else:
                self.game.soundAssets['fail50'].play()

            addEle = self.combo
            if self.prvElement == 0:
                self.fire += addEle
            elif self.prvElement == 1:
                self.water += addEle
            elif self.prvElement == 2:
                self.air += addEle
            elif self.prvElement == 3:
                self.lightening += addEle

            self.game.renderer.shake = min(self.combo/10, 300)
            self.combo = 0
        self.prvElement = element
        return


    def changeAct(self):
        self.game.soundAssets['change'].play()
        self.action += 1
        if self.action > 2:
            self.action = 0