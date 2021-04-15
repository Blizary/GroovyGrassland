import pygame
import os

#Script dedicated to loading images and other assets to be used by all other scripts

#Caption and Icon
icon = pygame.image.load(os.path.join('Assets', 'Plant1.png'))

#Background Image
backgroundImg = pygame.image.load(os.path.join('Assets', 'GroovyGrasslandBackground.png'))

#Plants and Pots Images
plantPotImg = pygame.image.load(os.path.join('Assets', 'PlantPot.png'))
plantStages = []
plantStages.append(pygame.image.load(os.path.join('Assets', 'Plant0.png')))
plantStages.append(pygame.image.load(os.path.join('Assets', 'Plant1.png')))
plantStages.append(pygame.image.load(os.path.join('Assets', 'Plant2.png')))
plantStages.append(pygame.image.load(os.path.join('Assets', 'Plant3.png')))

#Water and WaterTank Images
waterTankImg = pygame.image.load(os.path.join('Assets', 'WaterTower.png'))

#Player
playerImg = pygame.image.load(os.path.join('Assets', 'gardener.png'))
playerLife = pygame.image.load(os.path.join('Assets', 'ShovelLife.png'))
