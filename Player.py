import pygame
import os
import LoadAssets


class PLAYER:

    def __init__(self, pos, numOfLines,screen):
        self.image = LoadAssets.playerImg
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.currentLine = 0
        self.numOfLines = numOfLines
        self.maxlifes = 3
        self.currentlifes = 3
        self.screen = screen

    def PlayerMove(self, dir):

        if dir == True:
            if self.currentLine > 0:
                self.rect.top -= 48
                self.currentLine -= 1
        else:
            if self.currentLine < self.numOfLines-1:
                self.rect.top += 48
                self.currentLine += 1

    def RemoveLifes(self,amount):
        self.currentlifes -= amount
        print (self.currentlifes)

    def DrawLifes(self):
        for lifes in range(self.currentlifes):
            self.screen.blit(LoadAssets.playerLife,(10+14*lifes,10))