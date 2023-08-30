from scripts.utils import *

class Assets:
    def __init__(self):

        self.font = pygame.font.Font('resources/stardust.ttf')
        self.largeFont = pygame.font.Font('resources/stardust.ttf', 40)
        self.middleFont = pygame.font.Font('resources/stardust.ttf', 25)

        self.images = {
            'player/idle': Animation(load_images('entity/player'), img_dur=10),
            'ui/elements': load_images('ui/elements'),
            'ui/leftBtn.png': 0,
            'ui/rightBtn.png': 0,
            'ui/scrollMask.png': 0,
            'ui/leftBtnPressed.png': 0,
            'ui/rightBtnPressed.png': 0,
            'ui/mine.png': 0,
            'ui/upgrade.png': 0,
            'ui/move.png': 0,
            'ui/UIBG.png': 0,
            'ui/smallBtn.png': 0,
            'ui/smallBtnPressed.png': 0,
            'ui/dialog.png' : 0
            # 'ui/upgradeAdd' : 1
        }
        self.imagePreprocess()

        self.sounds = {
            'mineSpawn': pygame.mixer.Sound('resources/sound/mineSpawn.wav'),
            'mine': pygame.mixer.Sound('resources/sound/mine.wav'),
            'mineSpawnStart': pygame.mixer.Sound('resources/sound/mineSpawnStart.wav'),
            'jump': pygame.mixer.Sound('resources/sound/jump.wav'),
            'fail50': pygame.mixer.Sound('resources/sound/fail50.wav'),
            'fail200': pygame.mixer.Sound('resources/sound/fail200.wav'),
            'change': pygame.mixer.Sound('resources/sound/change.wav')
        }


    def imagePreprocess(self):
        for i in self.images:
            if self.images[i] == 0:
                self.images[i] = load_image(i)
            if i.startswith('ui/'):
                if i.endswith('.png'):
                    self.images[i] = pygame.transform.scale(self.images[i],
                                                            (self.images[i].get_width() * 3,
                                                             self.images[i].get_height() * 3))
                else:
                    for l in range(len(self.images[i])):
                        self.images[i][l] = pygame.transform.scale(self.images[i][l],
                                                                   (self.images[i][l].get_width() * 3,
                                                                    self.images[i][l].get_height() * 3))
                        self.images[i][l].set_alpha(70)