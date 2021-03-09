# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #get variables for current position
        currentPos = currentGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()
        foodList = currentFood.asList()
        #assign default values
        myScore = 0

        #calculate the distance to each piece of food
        for foodPos in foodList:
            #calculate manhattan distance of current pos to all the food
            foodMan = abs(newPos[0] - foodPos[0]) + abs(newPos[1] - foodPos[1])
            #next position may be attempted, add it after normalizing it
            if foodMan > 0:
                myScore += (1/foodMan)

        #calculate distance to each ghost
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            #calculate manhattan distance of current pos to the ghost
            ghostMan = abs(newPos[0] - ghostPos[0]) + abs(newPos[1] - ghostPos[1])
            #next position wont result in death, allow attempt
            if ghostMan > 1:
                myScore -= (1/ghostMan)
            #if the next step will kill pacman, set value as undesirable (negative infinity) so it wont get selected
            if ghostMan <= 1:
                myScore = -float('inf')

        #return the game score with the normalized food and ghost values
        return successorGameState.getScore() + myScore


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, depth, gameState):
            #check the ending conditions, if depth is reached or the game has been won or lost
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            #increment who is the agent
            nextAgent = agentIndex + 1
            #have reached the final ghost, set the next run back to pacman
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
                depth += 1
            #all possible actions
            actions = gameState.getLegalActions(agentIndex)
            #pacman, return maximum
            if agentIndex == 0:
                maxVal = -float('inf')
                for nextAction in actions:
                    val = minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                    maxVal = max(maxVal, val)
                return maxVal
            #not pacman, get the minimum
            else:  
                minVal = float('inf')
                for nextAction in actions:
                    val = minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                    minVal = min(minVal, val)
                return minVal
        #start the program off with pacman as the first agent
        maximum = -float('inf')
        #calculate for each successor to pacman
        for action in gameState.getLegalActions(0):
            #start the recursive stack on the next action
            value = minimax(1, 0, gameState.generateSuccessor(0, action))
            #take max of the returned value
            if value > maximum:
                maximum = value
                bestAction = action
        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction

        Description: This question asks to implement a minimax solution with alpha beta pruning added. This works the same
        as minimax except it adds additional efficiency because the subtrees that do not need to be explored are not,
        they get pruned. Alpha is the best option for max and Beta is the best option for the minimum. 
        The implementation works in a very similar mannor to minimax where the algorithm decides if the agent is 
        pacman or the ghost, and will choose to minimize or maximize the solution. If the agent is pacman, the 
        value will be maximized, if the agent is a ghost the value will be minimized. However, there is an additional 
        decision in this method, if the max value from pacmans route is greater than beta, the value gets 
        returned, thereby pruning that branch. If the value is smaller, alpha gets set to the new maximum. 
        Now if the agent a ghost, you check if the minimum value is less than alpha, if it is that branch gets
        returned and pruned. If it is not, beta gets set to the lowest between beta and the new minimum. The function
        that actually calls the alpha beta minimax needs extra logic aswell, since this part that initially calls
        the minimax is located outside minimax and uses a for loop, the values of alpha and beta are lost when the
        branch next to the root is called. Since the first call is always pacman, you can just take the smallest
        alpha value returned from minimax and set that as the next alpha that gets passed for the other branches 
        steming from the root.
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, depth, gameState, alpha, beta):
            #check the ending conditions, if depth is reached or the game has been won or lost
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            #increment who is the agent
            nextAgent = agentIndex + 1
            #have reached the final ghost, set the next run back to pacman
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
                depth += 1
            #all possible actions
            actions = gameState.getLegalActions(agentIndex)
            #pacman, return maximum
            if agentIndex == 0:
                maxVal = -float('inf')
                for nextAction in actions:
                    val = minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction), alpha, beta)
                    maxVal = max(maxVal, val)
                    #if max is larger than alpha, prune
                    if maxVal > beta:
                        return maxVal
                    #if not, change alpha to new largest
                    alpha = max(alpha, maxVal)
                return maxVal
            #not pacman, get the minimum
            else:  
                minVal = float('inf')
                for nextAction in actions:
                    val = minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction), alpha, beta)
                    minVal = min(minVal, val)
                    #if min is smaller than alpha, prune
                    if minVal < alpha:
                        return minVal
                    #is not, change beta to new smallest
                    beta = min(beta, minVal)
                return minVal
        #start the program off with pacman as the first agent
        maximum = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        #calculate for each successor to pacman
        for action in gameState.getLegalActions(0):
            #start the recursive stack on the next action
            value = minimax(1, 0, gameState.generateSuccessor(0, action), alpha, beta)
            if alpha < value:
                alpha = value
            #take max of the returned value
            if value > maximum:
                maximum = value
                bestAction = action
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.

        Description: The previous minimax algorithms assume that both agents will be working perfectly and in their best interest.
        However, this is not always the case, sometimes agents will choose a logically less effective solution or
        solutions at random which will mess up minimax. Expectimax takes into account that your opponent may act 
        irrationally and puts percentages on different outcomes. Pacman will still want to maximize the score but 
        ghosts have to be viewed as imperfect agents. When it is pacmans turn the implemention is the exact same 
        as minimax. When it is the ghosts turn, instead of taking the minimum value, all the values are added up 
        and divided by the number of actions explored. The problem statement said all values are equally random
        so this method of finding the average should be the value of each one being random. 
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, depth, gameState):
            #check the ending conditions, if depth is reached or the game has been won or lost
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            #increment who is the agent
            nextAgent = agentIndex + 1
            #have reached the final ghost, set the next run back to pacman
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
                depth += 1
            #all possible actions
            actions = gameState.getLegalActions(agentIndex)
            #pacman, return maximum
            if agentIndex == 0:
                maxVal = -float('inf')
                for nextAction in actions:
                    val = minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                    maxVal = max(maxVal, val)
                return maxVal
            #not pacman, get the average value assuming random probability
            else:  
                expectiVal = 0.0
                for nextAction in actions:
                    val = minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                    expectiVal += val
                #return the average value (all equal probability)
                return expectiVal / float(len(actions))
        #start the program off with pacman as the first agent
        maximum = -float('inf')
        bestAction = Directions.WEST
        #calculate for each successor to pacman
        for action in gameState.getLegalActions(0):
            #start the recursive stack on the next action
            value = minimax(1, 0, gameState.generateSuccessor(0, action))
            #take max of the returned value
            if value > maximum:
                maximum = value
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Similar to the first question in part one, this questions asks to implement an evaluation function. This one
    is based on the game state and not the action. I used a variety of methods to calculate the evaluation. The
    first method I used was the basic food. I calculated the manhattan distance to each piece of food then grabbed
    the closest one (smallest) and added that to my score after normalizing it. After the food, I wanted pacman to 
    favor getting the capsules, I used the same method as I did for the food except this time I multiplied the
    normalized value by 10, this meant that pacman should favor this value more than regualar food. The next section
    I tackled was the ghosts, being near ghosts is bad so I again calculated the manhattan distance to all ghosts 
    and took the closest one and this time subracted it from my score, this meant pacman should favor going away
    from ghosts more. I added a special case where if the move resulted in running into a ghost, the score would
    be set to negative infinity, therefore making it the least favorited solution (pacman should run away no matter 
    what). In the same ghost method I checked if the ghosts were in the scared state, and if they were I again added
    them to a list and took the closest one. When this value was added to my score I mulitplied it by 25 so that it
    should be the most favorable move to eat a scared ghost. 
    Finally, I was running into an issue where my ghost would get in a spot where he would get stuck in between two
    equal states so I added an element of randomness where I would add .1 with a 50% chance so that pacman would
    eventually pick on of the routes.
    """
    "*** YOUR CODE HERE ***"
    myScore = currentGameState.getScore()
    currentPos = currentGameState.getPacmanPosition()

    #food is good, get distance to closest food
    currentFood = currentGameState.getFood()
    foodList = currentFood.asList()
    if len(foodList) > 0:
        foodDist = []
        #calculete the manhattan distance to each piece of food
        for foodPos in foodList:
            foodDist.append(abs(currentPos[0] - foodPos[0]) + abs(currentPos[1] - foodPos[1]))
        #grab the closest food
        minFoodDist = min(foodDist)
        #avoid divide by 0
        if minFoodDist > 0:
            myScore += (1 / float(minFoodDist)) * 5


    #capsule is also good, get distance to closest pellet
    capsuleList = currentGameState.getCapsules()
    if len(capsuleList) > 0:
        capsuleDist = []
        #calculete the manhattan distance to each capsule
        for capsulePos in capsuleList:
            capsuleDist.append(abs(currentPos[0] - capsulePos[0]) + abs(currentPos[1] - capsulePos[1]))
        #grab the closest capsule
        minCapsuleDist = min(capsuleDist)
        #avoid divide by 0 and really favor the capsules (10x)
        if minCapsuleDist > 0:
            myScore += (1 / float(minCapsuleDist)) * 10


    #ghosts are bad, get distance to closest ghost, if next turn hits ghost, run away
    ghostStates = currentGameState.getGhostStates()
    if len(ghostStates) > 0:
        ghostDist = []
        scaredGhostDist = []
        #calculete the manhattan distance to each ghost
        for ghostSt in ghostStates:
            ghostPos = ghostSt.getPosition()
            ghostDist.append(abs(currentPos[0] - ghostPos[0]) + abs(currentPos[1] - ghostPos[1]))
            #if the ghost is scared, add it to the list
            if ghostSt.scaredTimer > 0:
                scaredGhostDist.append(abs(currentPos[0] - ghostPos[0]) + abs(currentPos[1] - ghostPos[1]))
        #grab the closest ghost
        minGhostDist = min(ghostDist)
        #if ghost will not kill in next move, allow it to continue
        if minGhostDist > 0:
            myScore -= (1 / float(minGhostDist))
        #if the next step will kill pacman, set value as undesirable (negative infinity) so it wont get selected
        if minGhostDist <= 0:
            myScore = -float('inf')
        #if there is a scared ghost, favor going after it (25x, the most favorable action)
        if len(scaredGhostDist) > 0:
            myScore += (1 / float(min(scaredGhostDist))) * 25

    #use a 50% coin flip to rid the situations where two routes have the same manhattan distance, it will force one to be selected eventually
    if util.flipCoin(.5):
        myScore += .1
    
     #return the game score with my calculations added on it
    return myScore


# Abbreviation
better = betterEvaluationFunction
