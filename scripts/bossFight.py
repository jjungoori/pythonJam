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
        self.pattern = [0,0,0,1,2]
        self.hp = 0

        self.bosses = self.game.gameManager.bosses

    def load(self):
        self.bosses = self.game.gameManager.bosses

    def start(self, type = -1):
        if type != -1:
            self.type = type

        self.game.gameManager.combo = 0
        self.boss = copy.deepcopy(self.bosses[self.type])
        self.hp = self.boss.hp
        self.boss.object = GameObject(Animation(load_images(self.boss.animationPath), 10),
                                      self.game.gameManager.player[0].pos + np.array((-70, 0)))
        self.excutePattern(self.boss.pattern[self.boss.nowAct])
        self.game.assets.sounds['bossSpawn'].play()
        # self.game.gameManager.objects.append(self.boss.object)

        if self.game.gameManager.action == 2:
            self.game.gameManager.changeAct()


        self.enable = True

    def playerAct(self, elements):
        if self.enable:
            if sum(elements) < 10:
                self.game.assets.sounds['res'].play()
                return

            self.hp -= sum(elements)
            if self.game.gameManager.playerAtt.attacker:
                self.hp -= sum(elements)

            self.pattern -= np.array(elements)
            if self.pattern[0] <= 0 and self.pattern[1] <= 0 and self.pattern[2] <= 0 and self.pattern[3] <= 0:

                self.nextPattern()

            if self.hp <= 0:
                print("tlqkf")
                self.win()

    def excutePattern(self, pattern):
        self.game.bossTimer.timers.clear()
        self.pattern = self.boss.pattern[self.boss.nowAct]
        self.game.bossTimer.add(pattern[4]*1000, self.attackPlayer)
        pass
    def attackPlayer(self):
        #attack
        self.game.gameManager.playerAttaked(sum(self.pattern)-self.pattern[4])
        self.nextPattern()
        self.game.assets.sounds['hitHurt'].play()
        print("attacked")
        if self.game.gameManager.playerAtt.hp <= 0:
            if self.game.gameManager.playerAtt.reviver:
                self.game.gameManager.combo += self.game.gameManager.playerAtt.hp
            self.game.gameManager.playerAtt.hp = self.game.gameManager.playerAtt.maxHP
            self.fail()

    def nextPattern(self):
        if self.boss.nowAct < len(self.boss.pattern)-1:
            self.boss.nowAct += 1
            self.excutePattern(self.boss.pattern[self.boss.nowAct])
            print("ff")

        else:
            self.boss.nowAct = 0

            self.excutePattern(self.boss.pattern[self.boss.nowAct])
            # self.nextPattern()
            print("ss")

    def fail(self):
        self.game.assets.sounds['die'].play()

        self.enable = False
        self.game.bossTimer.timers.clear()
        self.game.renderer.fadeInAndOut()

    def win(self):
        self.bosses[self.type].defeat = 1
        print("g")
        self.game.assets.sounds['kill'].play()
        self.enable = False
        self.game.bossTimer.timers.clear()

        self.game.gameManager.playerAtt.upgrades[self.boss.reward] = 0

        for i in range(100):
            print("k")
            self.game.gameManager.particles.append(
                Particle(self.boss.object.pos,
                         ((random.random() - 0.5) * 20, (random.random() - 0.5) * 20), 5.0,
                         random.random() + 0.01,
                         (random.random() * 255, random.random() * 255, random.random() * 255), 0, 0))

        # self.game.gameManager.objects.remove(self.boss.object)






class Boss:
    def __init__(self,name, hp, animationPath, damage, speed, pattern, reward):
        # super().__init__(animation, (20,20))

        self.name = name
        self.defeat = 0

        self.nowAct = 0
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.pattern = pattern
        self.animationPath = animationPath
        self.reward = reward

        self.object = None

    def __getstate__(self):
        state = self.__dict__.copy()

        delState = ['object']
        for i in delState:
            if i in state:
                del state[i]

        return state