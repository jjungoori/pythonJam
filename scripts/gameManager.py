# import curses

import  pygame
from scripts.objects import *
import  numpy as np
from scripts.utils import *
from scripts.renderer import ImageButton
class GameManager:

    def __init__(self, game):
        self.game = game

        self.menus = [
            Menu(self.game, [
                MenuItems(None,
                          ImageButton([game.assets['ui/smallBtn.png'], game.assets['ui/smallBtnPressed.png']],
                                      (0, 0), self.game.currentIsland.upgrade, 'add'), 'island', 'add 1 combo per click'),
            ]),
            Menu(self.game, [
                MenuItems(None,
                          ImageButton([game.assets['ui/smallBtn.png'], game.assets['ui/smallBtnPressed.png']],
                                      (0, 0), self.game.currentIsland.currentObject.upgrade, 'add'), 'mine',
                          'add 2 combo per click'),
            ]),
            Menu(self.game, [
                MenuItems(None,
                          ImageButton([game.assets['ui/smallBtn.png'], game.assets['ui/smallBtnPressed.png']],
                                      (0, 0), self.game.currentIsland.currentObject.upgrade, 'add'), 'new',
                          'add 1 combo per click'),
            ]),
        ]
        self.menuIndex = 0
        self.menu = self.menus[self.menuIndex]
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
            targetObject = self.game.currentIsland.currentObject
            if type(targetObject) == TileMine:
                if not targetObject.on:
                    if not targetObject.working:
                        targetObject.working = True
                        targetObject.spawnTileObject(self.game)
                else:
                    targetObject.mine(args[0])
        elif self.action == 1:
            if args[0] == 0:
                if self.game.currentIsland.currentObjectIndex > 0:

                    self.game.currentIsland.currentObjectIndex -= 1
                    self.game.currentIsland.sync()
                    targetObject = self.game.currentIsland.currentObject
                    self.game.player[0].pos = np.array(
                        tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[1], dtype=float)))
                elif self.game.currentIslandIndex > 0:
                    self.game.currentIslandIndex -= 1
                    self.game.currentIsland = self.game.islands[self.game.currentIslandIndex]

                    targetObject = self.game.currentIsland.currentObject
                    self.game.player[0].pos = np.array(
                        tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[1], dtype=float)))
            elif args[0] == 1:
                if self.game.currentIsland.currentObjectIndex < len(self.game.currentIsland.objects)-1:
                    self.game.currentIsland.currentObjectIndex += 1
                    self.game.currentIsland.sync()
                    targetObject = self.game.currentIsland.currentObject
                    self.game.player[0].pos = np.array(
                        tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[0], dtype=float)))
                elif self.game.currentIslandIndex < len(self.game.islands) - 1:
                    self.game.currentIslandIndex += 1
                    self.game.currentIsland = self.game.islands[self.game.currentIslandIndex]

                    targetObject = self.game.currentIsland.currentObject
                    self.game.player[0].pos = np.array(
                        tilePosToPos(targetObject.pos + np.array(targetObject.playerOffsetPos[1], dtype=float)))
        elif self.action == 2:
            if(args[0] == 1):
                self.menuIndex += 1
                if self.menuIndex > 2:
                    self.menuIndex = 0
                self.menu = self.menus[self.menuIndex]
                self.menu.on = True
            else:
                self.menu.on = False

    def mine(self, element):
        if self.prvElement == element:
            #calc added feature
            addedCombo = self.game.currentIsland.upgrades['add'] + self.game.currentIsland.currentObject.upgrades['add']
            self.combo += addedCombo
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


    def changeAct(self, *args):
        self.menu.on = False
        self.game.soundAssets['change'].play()
        self.action += 1
        if self.action > 2:
            self.action = 0


class MenuItems:
    def __init__(self, image, button, title, description):
        self.image = image
        self.button = button
        self.title = title
        self.description = description
class Menu:
    def __init__(self, game, items):
        self.on = False
        self.game = game
        self.items = items

    def upgrade(self, *args):
        self.game.currentIsland.upgrades[args[0]] += 1

    def updateFromMine(self):
