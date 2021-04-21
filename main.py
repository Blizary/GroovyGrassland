import pygame
import Player
import Plants
import Water
import LoadAssets
import ScoreText
import random
import Button
from collections import defaultdict

FPS =60
#Player or AI
# just a variable to control if it is a player playing or an AI
playerPlaying = False

#Moves
moves = ["Up", "Down", "Water", "Fill"]
LEARNING_RATE = 0.5
DISCOUNT_FACTOR = 0.8

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

class Controller(object):

    def on_move(self, state, move, new_state, score):
        pass

    def get_move(self, *args, **kwargs):
        raise RuntimeError("You didn't override getmove!")

class RandomController(Controller):

    def get_move(self, *args, **kwargs):
        return random.choice( moves )

class GreedyController(Controller):

    def __init__(self, policy = None):
        if not policy:
            policy = defaultdict( lambda: defaultdict( int ) )
        self.policy = policy
        self.history = []

    def state_value(self, state, fn = max):
        if not self.policy[state]:
            return 0
        return fn( self.policy[state].values() )

    def state_value_agg(self, fn = max):
        best = None
        for state in self.policy:
            value = self.state_value(state, fn)
            if best == None or value > best:
                best = value
        return best

    def Q(self, state, action):
        return self.policy[state][action]

    def min_state_value(self):
        value = 0
        for state in self.policy:
            value = min( value, self.state_value(state, min) )
        return value

    def on_move(self, state, action, new_state, reward):
        """When we move, update the Q-Learning table"""
        # update table
        Q = self.policy

        # Keep track of the history (for offline learning)
        # calculate features:
        # s_features = self.state_to_features(state)
        # sprime_features = self.state_to_features( new_state )
        # self.history.append( s_features + [action, reward] + sprime_features  )

        # find what the best predicted 'next reward' would have been
        max_succ = 0
        if Q[str(new_state)]:
            max_succ = max( Q[str(new_state)].values() )

        # update the table according to the Q-Learning equation
        Q[str(state)][action] = Q[str(state)][action] + LEARNING_RATE * ( reward + DISCOUNT_FACTOR * max_succ ) - Q[str(state)][action]
        self.state = new_state

    def get_move(self, state, **kwargs):
        if random.uniform(0, 1) < 0.2:
            return random.choice( moves )
        else:
            return self.exploit(state)

    def exploit(self, state):
        best_choice = None
        best_score = -10000

        for action in moves:
            act_score = self.policy[str(state)][action]
            if act_score > best_score or (act_score == best_score and random.choice( [False, True] ) ):
                best_choice = action
                best_score = act_score

        return best_choice

class ApproxController(Controller):

    def __init__(self, weights):
        self.weights = weights
        self.history = []

    def Q(self, state, action):
        features = self.getFeatures(state, action)

        if self.weights == None:
            self.weights = [ 0 ] * len(features)

        total = 0
        for j in range(0, len(features)):
            total += self.weights[j] * features[j]
        return total

    def QPrime(self, new_state):
        """Get best reward from a successor state"""
        bestValue = None
        for action in moves:
            value = self.Q(new_state, action)
            if bestValue == None or bestValue < value:
                bestValue = value
        return bestValue



    def getFeatures(self, state, action):

        features = []


        lowestplant = 100
        lowestPlantLine = 0
        currrentGarden = state["garden"]
        for (i, plantline) in enumerate(currrentGarden):
            for plant in range(len(plantline)-1):
                if plantline[plant] <= lowestplant:
                    lowestplant = plantline[plant]
                    lowestPlantLine = i

        playerLayer = state["player"]
        if action == "Up":
            if playerLayer>0:
                playerLayer -= 1
        elif action == "Down":
            if playerLayer<numbOfPlantsPerLine-1:
                playerLayer += 1
        elif action == "Water":
            if playerLayer== lowestPlantLine:

                for (i, plantline) in enumerate(currrentGarden):
                    difference = 2 if playerLayer == i else 0
                    for plant in range(len(plantline) - 1):
                        if plantline[plant]+ difference <= lowestplant:
                            lowestplant = plantline[plant]
                            lowestPlantLine = i

        playerdist = playerLayer - lowestPlantLine

        features.append(playerdist)
        # Things you could try:
        #
        # 1. Choosing suitable features for your game
        # 2. Seeing what affect different features have


        return features

    def on_move(self, state, action, new_state, reward):
        """When we move, store the value in the history"""

        # update the weights
        self.update( state, action, reward, new_state )

        # Things that you could try:
        #
        # 0. adjusting the parameters (discount factor, epsilon, learning rate)
        # 1. replacing the update / linear Q function with something from scikit-learn
        # 2. replacing epsilon greedy with something else
        # 3. bootstrapping the weights based on saved values (I initialise them to zero)
        #
        # Adaptions from DQN:
        # 1. store a history and update based on (a random batch) of the history
        # 2. Using a 'fixed' Q target for q prime (then updating it every few hundred iterations)

        # update the current state
        self.state = new_state


    def update(self, s, action, reward, s_prime, discountFactor=0.8, learningRate=0.001):
        """Adjust the weights to adapt to observations"""

        # 1. get the features for the starting state
        f = self.getFeatures(s, action)

        # 2. find the best next action from the successor state according to Q:
        max_successor = self.QPrime(s_prime)
        target = reward + discountFactor * max_successor
        error = target - self.Q( s, action )

        # 3. calculate the error for each feature
        errors = []
        for j in range(0, len(self.weights) ):
            errors.append( learningRate * f[j] * error )

        # 4. update the weights
        for i in range( 0, len(self.weights) ):
            self.weights[i] = self.weights[i] + errors[i]

    def get_move(self, state, **kwargs):
        """Actual policy for making moves"""
        if random.uniform(0, 1) < 0.3:
            return random.choice( moves )
        else:
            print(self.weights)
            return self.exploit( state )

    def exploit(self, state):
        """Choose best based on Q values"""
        best = (None, None)

        for action in moves:
            score = self.Q( state, action )
            if best[0] is None or score > best[1]:
                best = ( action, score )

        return best[0]



class Game():

    def __init__(self):

        self.wavesTimerInner = 5
        self.currentWave = 0
        self.gameState = 0
        self.mousepos = (0, 0)
        self.aiLoops = 5
        self.internalScore = 0


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
        score.ResetAmount()

    def WorldState(self):

        state = {}
        state["garden"] = []
        for lines in range(numbOfPlantLines):
            plant_line = []
            state["garden"].append(plant_line)
            for number in range(numbOfPlantsPerLine):
                plant_line.append(garden[lines].pots[number].plantLife)
            plant_line.append(garden[lines].waterTank.waterAmount)

        state["player"] = player.currentLine
        return state

    def PlantLoop(self):
        # check is plants died
        for lines in range(numbOfPlantLines):
            for number in range(numbOfPlantsPerLine):
                self.internalScore += garden[lines].pots[number].PlantDeath(player)

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


    def GameLoop(self,controller):

        # Ai playing
        if playerPlaying == False:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Jump all the menus
            if self.gameState == 0:
                self.gameState = 1

            #if self.aiLoops > 0:
            currentState = self.WorldState()
            oldscore = self.internalScore
            move = controller.get_move(currentState)

            if move == "Up":
                player.PlayerMove(True)
            elif move == "Down":
                player.PlayerMove(False)
            elif move == "Water":
                self.internalScore += sum(garden[player.currentLine].WaterPlants())
                garden[player.currentLine].waterTank.WateringPlants(0.1)
            elif move == "Fill":
                self.internalScore += garden[player.currentLine].waterTank.Filling(1)

            if player.currentlifes <= 0:
                self.ResetGame(player)
                self.aiLoops -= 1
            #else:
                #self.gameState = 2
                #print("ended ai loops")

            # Ai play loop

            self.PlantLoop()
            self.UpdatePlants()

            endState = self.WorldState()
            controller.on_move(currentState,move,endState,oldscore-self.internalScore)

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
    controller = ApproxController(None)


    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            game.PlayerInputs(event)
            if event.type == pygame.QUIT:
                running = False
        game.GameLoop(controller)

    pygame.quit()



if __name__ == "__main__":
    main()
