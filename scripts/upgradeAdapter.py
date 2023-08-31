class UpgradeAdapter:
    def __init__(self, game):
        self.game = game
        self.fire = 0
        self.water = 0
        self.air = 0
        self.lightening = 0
        self.add = 0

    def calc(self):
        if 'add' in self.game.gameManager.currentIsland.currentObject.upgrades:
            self.add = self.game.gameManager.mineUpgrades['add']['values'][
                self.game.gameManager.currentIsland.currentObject.upgrades['add']]

        if 'fireAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
            self.fire = self.game.gameManager.mineUpgrades['fireAdd']['values'][self.game.gameManager.currentIsland.currentObject.upgrades['fireAdd']]

        if 'waterAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
            self.water = self.game.gameManager.mineUpgrades['waterAdd']['values'][
                self.game.gameManager.currentIsland.currentObject.upgrades['waterAdd']]

        if 'airAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
            self.air = self.game.gameManager.mineUpgrades['airAdd']['values'][
                self.game.gameManager.currentIsland.currentObject.upgrades['airAdd']]



        if 'bFireAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
            self.fire = self.game.gameManager.mineUpgrades['bFireAdd']['values'][self.game.gameManager.currentIsland.currentObject.upgrades['bFireAdd']]

        if 'bWaterAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
            self.water = self.game.gameManager.mineUpgrades['bWaterAdd']['values'][
                self.game.gameManager.currentIsland.currentObject.upgrades['bWaterAdd']]

        if 'bAirAdd' in self.game.gameManager.currentIsland.currentObject.upgrades:
            self.air = self.game.gameManager.mineUpgrades['bAirAdd']['values'][
                self.game.gameManager.currentIsland.currentObject.upgrades['bAirAdd']]