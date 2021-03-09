# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.

        DESCRIPTION: This question asks to implement a value iteration algorithm. 
        This will iterate through the pacman/gridword environment and update the 
        values of each square for each iteration. This is done by getting the actions 
        for each state and then calculating the Q values using the formula from class 
        which takes the probability of entering that state and multiplies that value 
        by the reward + the discounted reward. This value gets saved in the temporary 
        values which will eventually be saved in the actual self.values. This temporary 
        storage is to limit the depth that the squares get updated. If self.values was 
        updated immediately, the subsequent calls would use the value just inputted, so 
        for iteration 1, all values would be filled instead of only the exit square.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #loop through k times
        for i in range(self.iterations):
            states = self.mdp.getStates()
            #make a copy of values to keep the depth at k and not the full values
            valuesCopy = self.values.copy()
            #get the actions for each state
            for state in states:
                actions = self.mdp.getPossibleActions(state)
                qList = []
                #calculate the q value for each action
                for action in actions:
                    qList.append(self.computeQValueFromValues(state, action))
                #set the value to the max q value (v value) (if its not empty)
                if qList:
                    valuesCopy[state] = max(qList)
            #save the value results into self.values
            self.values = valuesCopy



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #initilize value and get the possible outcomes/percentages from the position
        value = 0
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        #add the q value for each possible outsome with the percentage
        for nextState, probability in transitions:
            #calculate the q value and add to the value
            value += (probability * (self.mdp.getReward(state, action, nextState) + (self.discount * self.values[nextState])))
        #return the q value
        return value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        #look at all possible options, which is k+1, calculate the q value, and return the direction of the max

        #return none if its on the terminal state
        if self.mdp.isTerminal(state):
            return None
        #set default values/worst case scenarios
        bestVal = -float('inf')
        bestAction = None
        #get the qValue for each action and return the action that has the largest qValue
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            qVal = self.computeQValueFromValues(state, action)
            if qVal > bestVal:
                bestVal = qVal
                bestAction = action
        return bestAction


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.

        DESCRIPTION: This question is very similar to question one, 
        the main difference here is that only one state is updated per 
        iteration, the line “state = states[i % len(states)]” determines 
        the state that gets updated.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #loop through k times
        for i in range(self.iterations):
            states = self.mdp.getStates()
            #grab only the current state, use i mod number of states
            state = states[i % len(states)]
            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)
                qList = []
                #calculate the q value for each action
                for action in actions:
                    qList.append(self.computeQValueFromValues(state, action))
                #set the value to the max q value (v value) (if list not empty)
                if qList:
                    self.values[state] = max(qList)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.

        DESCRIPTION: This question asks to implement a prioritized sweeping value 
        iteration. The logic for calculating the q value is very similar to question 
        1, however this question favors the squares that are most likely to result 
        in a changed value. This is determined by using a difference value between 
        the current value of the state and the highest q value. This difference value 
        then gets put in the priority queue as a negative so the pop function will 
        take the one with the highest error value. This question also uses predecessors 
        which is the state that came before the current state, this is found by storing 
        each state in a dictionary and having the predecessor state as its entries. 
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #initilize empty structures
        prioQueue = util.PriorityQueue()
        predecessors = dict()

        #compute all predecessors (non 0 percentage)
        states = self.mdp.getStates()
        for state in states:
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                transitions = self.mdp.getTransitionStatesAndProbs(state, action)
                for nextState, probability in transitions:
                    #add the predecessor if the proablility is not 0
                    if probability > 0:
                        #if its the first element of nextState, create set, then add to it
                        if nextState not in predecessors:
                            predecessors[nextState] = set()
                        predecessors[nextState].add(state)

        #for each non-terminal state in states
        for state in states:
            if not self.mdp.isTerminal(state):
                #calculate the difference between current value of s and hightest q-value
                #(next 4 lines calculate max q value)
                qList = []
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                        qList.append(self.computeQValueFromValues(state, action))
                diff = abs(self.values[state] - max(qList))
                prioQueue.update(state, -diff)  #use update so it takes the highest error value

        #for iteration, do...
        for i in range(self.iterations):
            #if prio queue is empty, terminate
            if prioQueue.isEmpty():
                break
            state = prioQueue.pop()
            #if the state is not terminal, update the value of the state
            if not self.mdp.isTerminal(state):
                #(next 4 lines calculate max q value)
                qList = []
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    qList.append(self.computeQValueFromValues(state, action))
                self.values[state] = max(qList)

            #for each predecessor, find the difference between current value and highest q value
            for predecessor in predecessors[state]:
                #(next 4 lines calculate max q value)
                currQList = []
                actions = self.mdp.getPossibleActions(predecessor)
                for action in actions:
                    currQList.append(self.computeQValueFromValues(predecessor, action))
                diff = abs(self.values[predecessor] - max(currQList))
                if diff > self.theta:
                    prioQueue.update(predecessor, -diff)    #use update so it takes the highest error value



