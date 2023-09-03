from scripts.UIManager import *

class DialogManager:
    def __init__(self, game):
        self.dialogs = [
            # "hello my name is chick",
            # "I love you man",
            # "aya",
            # "hoohohjohjaiojsdiofjosidf",
            # "hello my name is chick"
        ]
        self.behavior = 0
        self.game = game

    def setDialog(self, text):
        self.dialogs = text.split('\n')

    def next(self):
        if len(self.dialogs) > 0:
            self.game.UIManager.dialog.on = True
            if self.behavior == 0:
                self.game.UIManager.dialog.say(self.dialogs[0], 50)
                self.game.UITimer.add(50*len(self.dialogs[0]), lambda x=1 : self.setBehavior(2))
                self.setBehavior(1)
            elif self.behavior == 1:
                self.game.UIManager.dialog.print(self.dialogs[0])
                self.setBehavior(2)
            elif self.behavior == 2:
                self.dialogs.pop(0)
                self.setBehavior(0)
                self.next()
        else:
            self.game.UIManager.dialog.on = False


    def setBehavior(self, b):
        self.behavior = b