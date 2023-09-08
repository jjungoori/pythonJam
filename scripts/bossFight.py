from scripts.objects import *
import  numpy as np
import  copy
from scripts.timer import  *
class BossManager:
    def __init__(self, game):
        self.game = game
        self.enable = False
        self.type = 0
        self.boss = None
        self.pattern = [0,0,0,1,2,3]

        self.bosses = [
            Boss( 0, self.game.assets.images['boss1'], 1, 1, pattern=[
                [0, 0, 0, 1, 1, 2], #1, 2, 3, 4 : elements, 5 damage, 6 time
                [1, 0, 0, 0, 5, 10]
            ])
        ]

    def start(self):
        self.boss = copy.deepcopy(self.bosses[self.type])
        self.game.gameManager.objects.append(self.boss)
        self.enable = True

    def playerAct(self, elements):
        if self.enable:
            self.boss.hp -= sum(elements)
            self.pattern -= np.array(elements)
            if self.pattern[0] <= 0 and self.pattern[1] <= 0 and self.pattern[2] <= 0 and self.pattern[3] <= 0:
                self.game.bossTimer.timers.clear()
                self.nextPattern()

            if self.boss.hp <= 0:
                self.win()

    def excutePattern(self, pattern):
        self.game.bossTimer.add(pattern[5], self.attackPlayer)
        pass
    def attackPlayer(self):
        #attack
        self.nextPattern()

    def nextPattern(self):
        if self.boss.nowAct < len(self.boss.pattern):

            self.excutePattern(self.boss.pattern[self.boss.nowAct])
            self.boss.nowAct += 1

        else:
            self.boss.nowAct = 0
            self.nextPattern()

    def fail(self):
        pass
    def win(self):
        pass





class Boss(GameObject):
    def __init__(self, hp, animation, damage, speed, pattern):
        super().__init__(animation, (20,20))

        self.nowAct = 0
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.pattern = pattern
