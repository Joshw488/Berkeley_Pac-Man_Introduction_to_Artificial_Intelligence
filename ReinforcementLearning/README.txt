Author:		Josh Watts
Date:		February 26th, 2021
Assignment:	CSS382 Project 3 - Reinforcement Learning

Description: This project introduces reinforcement learning in the form of q-learning. This adds the functionality
for pacman to learn from previous actions, pacman will run for a provided number of iterations and use a combination
of exploration and exploitation to find the optimal path.

--------------------------------Question 1: Value Iteration--------------------------------------------
This question asks to implement a value iteration algorithm. This will iterate through the pacman/gridword 
environment and update the values of each square for each iteration. This is done by getting the actions 
for each state and then calculating the Q values using the formula from class which takes the probability 
of entering that state and multiplies that value by the reward + the discounted reward. This value gets 
saved in the temporary values which will eventually be saved in the actual self.values. This temporary 
storage is to limit the depth that the squares get updated. If self.values was updated immediately, the 
subsequent calls would use the value just inputted, so for iteration 1, all values would be filled instead 
of only the exit square.

--------------------------------Question 2: Bridge Crossing Analysis--------------------------------------------
This question asks to find the optimal policy for pacman to cross a bridge where both sides are pits of fire. The
optimal parameter to tweak is the noise because allowing pacman to succeed in every action gaurantees they wont
fall in the pit of fire on accident. 

--------------------------------Question 3: Policies--------------------------------------------
This question ask to find the optimal parameters for different scenarior to happen. 
Prefer the close exit (+1), risking the cliff (-10)
	Big discount so the agent prefers things closer, no noise means the agent can 
	go close to the pit without worrying about an accidental fall
Prefer the close exit (+1), but avoiding the cliff (-10)
	Big discount means closer things should be favored, added noise so there is a 
	possibility of falling in the pit, so agent will avoid it
Prefer the distant exit (+10), risking the cliff (-10)
	Favor going far but with 100% success in actions, pacman can go by the cliff without falling in
Prefer the distant exit (+10), avoiding the cliff (-10)
	Favor going far but having noise means the cliff could result in death so it should be avoided
Avoid both exits and the cliff (so an episode should never terminate)
	The living reward would always be greater than an exit

--------------------------------Question 4: Asynchronous Value Iteration--------------------------------------------
This question is very similar to question one, the main difference here is that only one state is updated per 
iteration, the line “state = states[i % len(states)]” determines the state that gets updated.

--------------------------------Question 5: Prioritized Sweeping Value Iteration------------------------------------
This question asks to implement a prioritized sweeping value iteration. The logic for calculating the q value is 
very similar to question 1, however this question favors the squares that are most likely to result in a changed 
value. This is determined by using a difference value between the current value of the state and the highest q 
value. This difference value then gets put in the priority queue as a negative so the pop function will take the 
one with the highest error value. This question also uses predecessors which is the state that came before the 
current state, this is found by storing each state in a dictionary and having the predecessor state as its entries. 

--------------------------------Question 6/7: Q-Learning--------------------------------------------
This question starts to implement q learning, which unlike the first couple questions, learns from experience 
rather than calculating the best route before moving. In this question, the agent will move around the world 
constantly updating the q values. There is an extra epsilon and alpha value. The epsilon value is how often 
the agent will take a random move, the alpha value is how great of an effect new samples have on the values. 
When choosing the action the epsilon has to be used, to do this the code will take a random number between 
between 0 and 1 and if that value is within the epsilon, the action returned will be randomly chosen, if the 
value is not within the epsilon, then the highest (best) action is returned. The computation happens by 
getting the action, calculating the q values, and taking the max.

--------------------------------Question 8: Bridge Crossing Revisited--------------------------------------------
This question asks to change the q-learing parameters to get pacman to learn to cross the bridge. This problem has
no solution because the provided number of iteration (50) is not enough for pacman to properly learn that crossing
the bridge by going east continuously is optimal. 

--------------------------------Question 9: Q-Learning and Pacman--------------------------------------------
Solved earlier. 

--------------------------------Question 10: Approximate Q-Learning--------------------------------------------
This question is much like question 6 except the value that gets updated is based on different features instead 
of solely the state and action. Using just the state and action means the algorithm cannot generalize at all, 
using features means that if the agent gets in a situation similar (not exactly the same state) to one it has 
already seen, it can generalize the best move based on previous runs. This happens by calculating the difference 
between the expected value and the value that was actually received. This difference value then gets added to 
the saved weighted values which is set for each feature. The q value is determined by multiplying the feature 
by the weights.