import pygame
import os
import Water
import LoadAssets
import Player
import ScoreText
import random


class PLANTPOT:

    def __init__(self, pos, screen, score):
        self.image = LoadAssets.plantPotImg
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.plantState = 0
        self.plantImg = LoadAssets.plantStages[self.plantState]
        self.plantLife = 100
        self.screen = screen
        self.growthTimer = 30
        self.growthTimerInner = self.growthTimer
        self.score = score
        self.maxHealthBarSize = 20
        self.currentHealthBarSize = 20
        self.plantTick = 5
        self.plantTickInner = 5

    # updates the state and changes the sprite
    def UpdatePlantStage(self, newState):
        self.plantState = newState
        if newState==1:
            self.plantLife = random.randint(30, 70)
        self.plantImg = LoadAssets.plantStages[self.plantState]


    # checks if the plant died
    def PlantDeath(self,player):
        if self.plantLife <= 0:
            print("Plant death")
            player.RemoveLifes(1)
            # reset
            self.UpdatePlantStage(0)
            self.plantLife = 70
            return -100
        return 0

    def PlantLife(self):
        if self.plantState != 0:
            if self.plantTickInner <= 0:
                self.plantTickInner = self.plantTick
                if self.plantLife > 0:
                    self.plantLife -= 1
                    self.currentHealthBarSize = (self.plantLife * self.maxHealthBarSize)/100
            else:
                self.plantTickInner -= 1


    # draws the plants
    def DrawPlantPot(self):
        self.screen.blit(self.image, self.rect)
        if self.plantState != 0:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x+8, self.rect.y-7, 20, 5))
            pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x+8, self.rect.y -7, self.currentHealthBarSize, 5))
            self.screen.blit(self.plantImg, self.rect)

    # called when the plants are being watered, increases life to a max of 100
    def WaterPlant(self,amount):
        if self.plantState !=0:
            if self.plantLife < 100:
                self.plantLife += amount
                return 5
        return 0

    #Reset plant back to original state of the game
    def ResetPlant(self):
        self.plantLife = 100
        self.plantState = 0
        self.currentHealthBarSize = 20

    # general update function of the obj, contains the timer for the plant growth and calls other functions
    def Update(self):
        self.PlantLife()
        
        if self.plantState !=0:
            if self.growthTimerInner > 0:
                self.growthTimerInner -= 0.1
            else:
                self.growthTimerInner = self.growthTimer
                if self.plantState < len(LoadAssets.plantStages)-1:
                    self.plantState += 1
                    self.UpdatePlantStage(self.plantState)
                else:
                    self.UpdatePlantStage(0)
                    #reset
                    self.plantLife = 100
                    self.score.ChangeAmount(10)
                    self.score.UpdateText()



class PLANTLINE:
    def __init__(self, numOfPots, posY, screen, score):
        self.pots = []
        self.y = posY
        self.waterTank = Water.WATERTOWER((320, posY),screen)
        self.numOfPots = numOfPots
        self.score = score
        for number in range(numOfPots):
            newPlantPot = PLANTPOT((64 + 48*number, posY), screen, self.score)
            self.pots.append(newPlantPot)

    def WaterPlants(self):
        score = []
        for number in range(self.numOfPots):
            score.append(self.pots[number].WaterPlant(5))
        return score

    def ResetPlantLines(self):
        for number in range(self.numOfPots):
            self.pots[number].ResetPlant()
        self.waterTank.ResetTank()