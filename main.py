import pygame
import Player
import Plants
import Water
import LoadAssets
import ScoreText
import random
import Button

# Initialize pygame
pygame.init()

# Caption and Icon
pygame.display.set_caption("Groovy Grasslands")
pygame.display.set_icon(LoadAssets.icon)

# create screen
width = 352
heigh = 288
screen = pygame.display.set_mode((width, heigh))

# Buttons
playButton = Button.BUTTON((255,255,255),120,120,110,40,"Play")
retryButton = Button.BUTTON((255,255,255),120,120,110,40,"Retry")


# Score
pygame.font.init()
font = pygame.font.Font('Regular.ttf', 32)
score = ScoreText.TEXT(0, font, (150, 5), (0,0,0), screen)

#Other messages
failedGame = ScoreText.TEXT("Too many plants died", font, (50, 60), (0,0,0), screen)

# Waves
waves = [1, 3, 4, 2, 8, 2, 5, 8, 10]


# Plant Lines
numbOfPlantsPerLine = 4
numbOfPlantLines = 4
firstLineY = 80
garden = []
for number in range(numbOfPlantLines):
    garden.append(Plants.PLANTLINE(numbOfPlantsPerLine, firstLineY+48*number, screen, score))


# Player
player = Player.PLAYER((290, firstLineY), numbOfPlantLines,screen)





#Draw function
def draw_window(state):
    screen.blit(LoadAssets.backgroundImg, (0, 0))
    screen.blit(player.image, player.rect)
    screen.blit(score.texture, score.pos)
    player.DrawLifes()

    for lines in range(numbOfPlantLines):
        for number in range(numbOfPlantsPerLine):
            garden[lines].pots[number].DrawPlantPot()
        garden[lines].waterTank.DrawTank()

    if state == 0:
        playButton.draw(screen, None)

    if state == 2:
        screen.blit(failedGame.texture, failedGame.pos)
        retryButton.draw(screen, None)

    pygame.display.update()

def StartGame(state):
    state = 1


def UpdatePlants():

    for lines in range(numbOfPlantLines):
        for number in range(numbOfPlantsPerLine):
            garden[lines].pots[number].Update()



def PickRandPlant():
    plantsAvailable = []
    for plant in range(len(garden)):
        for pot in range (len(garden[plant].pots)):
            if garden[plant].pots[pot].plantState == 0:
                plantsAvailable.append(garden[plant].pots[pot])

    if len(plantsAvailable)!= 0:
        randInt = random.randint(0, len(plantsAvailable)-1)
        randPlant = plantsAvailable[randInt]
        return randPlant
    else:
        return -1



FPS =60

#Game loop
def main():
    clock = pygame.time.Clock()
    wavesTimer = 40
    wavesTimerInner = 5
    currentWave = 0
    gameState = 0
    mousepos = (0,0)

    running = True
    while running:
        clock.tick(FPS)
        # if key is pressed
        keysPressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            mousepos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False

            if gameState == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.isOver(mousepos):
                        gameState =1

            if gameState ==1:
                if keysPressed[pygame.K_DOWN]:
                    player.PlayerMove(False)
                if keysPressed[pygame.K_UP]:
                    player.PlayerMove(True)



        if gameState == 1:
            if keysPressed[pygame.K_RIGHT]:
                garden[player.currentLine].WaterPlants()
                garden[player.currentLine].waterTank.WateringPlants(0.1)
            elif keysPressed[pygame.K_SPACE]:
                garden[player.currentLine].waterTank.Filling(1)


            #check is plants died
            for lines in range(numbOfPlantLines):
                for number in range(numbOfPlantsPerLine):
                    garden[lines].pots[number].PlantDeath(player)
            if player.currentlifes <=0:
                gameState = 2

            #algo for plants
            if wavesTimerInner <= 0:
                for plant in range(waves[currentWave]):
                    randPlant = PickRandPlant()
                    if randPlant != -1:
                        randPlant.UpdatePlantStage(1)
                wavesTimerInner = wavesTimer
                if currentWave == len(waves)-1:
                    currentWave = 0
                else:
                    currentWave +=1
            else:
                wavesTimerInner -= 0.1



            UpdatePlants()
        draw_window(gameState)
    pygame.quit()



if __name__ == "__main__":
    main()
