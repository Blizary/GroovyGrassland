import pygame
import LoadAssets

class WATERTOWER:
    def __init__(self,pos,screen):
        self.image = LoadAssets.waterTankImg
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.waterAmount = 100
        self.screen = screen
        self.maxWaterLvl = 20
        self.currentWaterLvl =20

    def WateringPlants(self, amount):
        if self.waterAmount !=0:
            self.waterAmount -= amount
            self.currentWaterLvl = (self.waterAmount * self.maxWaterLvl) / 100



    def Filling(self, amount):
        if self.waterAmount <100:
            self.waterAmount += amount
            self.currentWaterLvl = (self.waterAmount * self.maxWaterLvl) / 100
            return 1
        return 0

    def DrawTank(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x + 8, self.rect.y - 7, 20, 5))
        pygame.draw.rect(self.screen, (0, 0, 255), (self.rect.x + 8, self.rect.y - 7, self.currentWaterLvl, 5))
        self.screen.blit(self.image, self.rect)

    #reset water levels to original amount
    def ResetTank(self):
        self.waterAmount =100
        self.currentWaterLvl = 20
