# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state

        
       DESCRIPTION: This question starts to implement q learning,
       which unlike the first couple questions, learns from experience 
       rather than calculating the best route before moving. In this question, 
       the agent will move around the world constantly updating the q values. 
       There is an extra epsilon and alpha value. The epsilon value is how often 
       the agent will take a random move, the alpha value is how great of an 
       effect new samples have on the values. When choosing the action, the 
       epsilon has to be used, to do this the code will take a random number 
       between between 0 and 1 and if that value is within the epsilon, the action 
       returned will be randomly chosen, if the value is not within the epsilon, 
       then the highest (best) action is returned (Greedy Epsilon). The computation 
       happens by getting the action, calculating the q values, and taking the max.
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qValues = util.Counter() # A Counter is a dict with default 0

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if not self.qValues[(state,action)]:
            return 0.0
        return self.qValues[(state,action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        maxVal = -float('inf')
        #get all the actions from the current state
        actions = self.getLegalActions(state)
        #if there are no actions, return 0.0
        if not actions:
            return 0.0
        for action in actions:
            #get all the qvalues for the state & action pair and take the largest one
            qVal = self.getQValue(state, action)
            if qVal > maxVal:
                maxVal = qVal
        return maxVal

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        maxVal = -float('inf')
        maxAction = None
        #get all the actions from the current state
        actions = self.getLegalActions(state)
        #if there are no actions, return none
        if not actions:
            return None
        for action in actions:
            #get all the qvalues for the state & action pair and take the largest one
            qVal = self.getQValue(state, action)
            if qVal > maxVal:
                maxVal = qVal
                maxAction = action
        return maxAction


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        #if there are no legal actions (terminal state), return none
        if not legalActions:
            return None
        #use probability epsilon, if it succeeds, choose a random action
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        #if not, take the best policy
        else:
            action = self.computeActionFromQValues(state)
        #return action, best choice or random
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #using formula: (1 - alpha) * oldValue + alpha * (reward + discounted future reward) 
        self.qValues[(state,action)] = ((1 - self.alpha) * self.getQValue(state,action) + self.alpha * (reward + (self.discount * self.computeValueFromQValues(nextState))))

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.

       DESCRIPTION: This question is much like question 6 except the value 
       that gets updated is based on different features instead of solely 
       the state and action. Using just the state and action means the 
       algorithm cannot generalize at all, using features means that if the 
       agent gets in a situation similar (not exactly the same state) to 
       one it has already seen, it can generalize the best move based on 
       previous runs. This happens by calculating the difference between 
       the expected value and the value that was actually received. This 
       difference value then gets added to the saved weighted values which 
       is set for each feature. The q value is determined by multiplying 
       the feature by the weights.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        #calculate and return the weighted score of the feature vector
        features = self.featExtractor.getFeatures(state, action)
        return features * self.weights

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        #use the difference formula from the lecture to calculate the difference between "what I thought id get and what I appear to be getting"
        diff = (reward + (self.discount * self.getValue(nextState))) - self.getQValue(state,action)
        #update the weighted values
        for feature in features:
            self.weights[feature] += self.alpha * diff


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
