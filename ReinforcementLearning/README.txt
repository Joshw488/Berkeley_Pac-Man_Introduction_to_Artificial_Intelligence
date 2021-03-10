Author:		Josh Watts
Date:		February 3rd, 2021
Assignment:	CSS382 Project 2 - Multi-Agent Search - P2

Description: This project introduces ghosts which work to defeat pacman. This program will explore
mulitple methods to win the game while now also working to stay alive. Pacman wins the game by eating
all the dots and staying alive and ghosts win the game by eating pacman. Part 1 of this project will
add three algorithms, one being a more advanced evaluation function that uses the current state, and 
the other two building on top of the minimax algorithm.

--------------------------------Question 3: Alpha-Beta Pruning--------------------------------------------
This question asks to implement a minimax solution with alpha beta pruning added. This works the same
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

--------------------------------Question 4: Expectimax--------------------------------------------
The previous minimax algorithms assume that both agents will be working perfectly and in their best interest.
However, this is not always the case, sometimes agents will choose a logically less effective solution or
solutions at random which will mess up minimax. Expectimax takes into account that your opponent may act 
irrationally and puts percentages on different outcomes. Pacman will still want to maximize the score but 
ghosts have to be viewed as imperfect agents. When it is pacmans turn the implemention is the exact same 
as minimax. When it is the ghosts turn, instead of taking the minimum value, all the values are added up 
and divided by the number of actions explored. The problem statement said all values are equally random
so this method of finding the average should be the value of each one being random. 

--------------------------------Question 5: Better Evaluation Function--------------------------------------------
Similar to the first question in part one, this questions asks to implement an evaluation function. This one
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

