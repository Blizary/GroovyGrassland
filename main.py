import pygame
import Player
import Plants
import Water
import LoadAssets
import ScoreText
import random
import Button


FPS =60
#Player or AI
# just a variable to control if it is a player playing or an AI
playerPlaying = True

#Moves
moves = ["Up", "Down", "Water", "Fill"]

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
wavesTimer = 40


# Plant Lines
numbOfPlantsPerLine = 4
numbOfPlantLines = 4
firstLineY = 80
garden = []
for number in range(numbOfPlantLines):
    garden.append(Plants.PLANTLINE(numbOfPlantsPerLine, firstLineY+48*number, screen, score))


# Player
player = Player.PLAYER((290, firstLineY), numbOfPlantLines,screen)



class Game():

    def __init__(self):

        self.wavesTimerInner = 5
        self.currentWave = 0
        self.gameState = 0
        self.mousepos = (0, 0)
        self.aiLoops = 5

    # Draw function
    def draw_window(self):
        screen.blit(LoadAssets.backgroundImg, (0, 0))
        screen.blit(player.image, player.rect)
        screen.blit(score.texture, score.pos)
        player.DrawLifes()

        for lines in range(numbOfPlantLines):
            for number in range(numbOfPlantsPerLine):
                garden[lines].pots[number].DrawPlantPot()
            garden[lines].waterTank.DrawTank()

        if self.gameState == 0:
            playButton.draw(screen, None)

        if self.gameState == 2:
            screen.blit(failedGame.texture, failedGame.pos)
            retryButton.draw(screen, None)

        pygame.display.update()

    def UpdatePlants(self):

        for lines in range(numbOfPlantLines):
            for number in range(numbOfPlantsPerLine):
                garden[lines].pots[number].Update()

    def PickRandPlant(self):
        plantsAvailable = []
        for plant in range(len(garden)):
            for pot in range(len(garden[plant].pots)):
                if garden[plant].pots[pot].plantState == 0:
                    plantsAvailable.append(garden[plant].pots[pot])

        if len(plantsAvailable) != 0:
            randInt = random.randint(0, len(plantsAvailable) - 1)
            randPlant = plantsAvailable[randInt]
            return randPlant
        else:
            return -1

    def ResetGame(self, player):

        print("reseting game")
        # reseting plants
        for lines in range(numbOfPlantLines):
            for number in range(numbOfPlantsPerLine):
                garden[lines].ResetPlantLines()

        player.currentlifes = player.maxlifes
        self.wavesTimerInner = 5
        self.currentWave = 0
        self.gameState = 1


    def PlantLoop(self):
        # check is plants died
        for lines in range(numbOfPlantLines):
            for number in range(numbOfPlantsPerLine):
                garden[lines].pots[number].PlantDeath(player)

        # algo for plants
        if self.wavesTimerInner <= 0:
            for plant in range(waves[self.currentWave]):
                randPlant = self.PickRandPlant()
                if randPlant != -1:
                    randPlant.UpdatePlantStage(1)
            self.wavesTimerInner = wavesTimer
            if self.currentWave == len(waves) - 1:
                self. currentWave = 0
            else:
                self.currentWave += 1
        else:
            self.wavesTimerInner -= 0.1

    def PlayerInputs(self, event):

        if playerPlaying == True:

            keysPressed = pygame.key.get_pressed()

            self.mousepos = pygame.mouse.get_pos()

            #Buttons
            if self.gameState == 0 or self.gameState == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.gameState == 0 and playButton.isOver(self.mousepos):
                        self.gameState = 1

                    if self.gameState == 2 and retryButton.isOver(self.mousepos):
                        self.ResetGame(player)



            if self.gameState == 1:
                if keysPressed[pygame.K_DOWN]:
                    player.PlayerMove(False)
                if keysPressed[pygame.K_UP]:
                    player.PlayerMove(True)


    def GameLoop(self):

        # Ai playing
        if playerPlaying == False:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Jump all the menus
            if self.gameState == 0:
                self.gameState = 1

            if self.aiLoops > 0:
                if player.currentlifes <= 0:
                    self.ResetGame(player)
                    self.aiLoops -= 1
            else:
                self.gameState = 2
                print("ended ai loops")

            # Ai play loop
            if self.gameState == 1:
                self.PlantLoop()
                self.UpdatePlants()


        # player playing
        else:
            # Inputs
            # if key is pressed
            keysPressed = pygame.key.get_pressed()

            if self.gameState == 1:
                if keysPressed[pygame.K_RIGHT]:
                    garden[player.currentLine].WaterPlants()
                    garden[player.currentLine].waterTank.WateringPlants(0.1)
                elif keysPressed[pygame.K_SPACE]:
                    garden[player.currentLine].waterTank.Filling(1)

                # Player Gameloop
                self.PlantLoop()
                self.UpdatePlants()
                if player.currentlifes <= 0:
                    self.gameState = 2

        self.draw_window()



#Game loop
def main():
    clock = pygame.time.Clock()
    game = Game()


    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            game.PlayerInputs(event)
            if event.type == pygame.QUIT:
                running = False
        game.GameLoop()

    pygame.quit()



if __name__ == "__main__":
    main()
