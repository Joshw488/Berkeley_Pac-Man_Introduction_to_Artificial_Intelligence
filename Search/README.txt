Author:		Josh Watts
Date:		January 16th, 2021
Assignment:	CSS382 Project 1 - Search

Description: This project explores different ways to implement search and heuristic functions 
using pacman as the environment. In this project you will find depth first search, breadth first
search, uniform cost search, and A* search. There are also addition functions like finding all
corners, finding all food, and heurictics for each.

---------------------------Question 1: Depth First Search---------------------------------------
This question asks for an implementation of a depth first search to find a fixed dot at a goal.
This function returns a list of actions that can be used by pacman to find the dot inside the maze.
Dfs plunges as deep as it can in the maze and if it hits a dead end, it backtracks to the next turn
and starts from there. 
This function works by implementing a standard stack and list that is used like a set. To begin
this function the starting position is added to the stack and then it enters the while loop that
runs until the path is returned. Each iteration of the loop the variables (state, actions, cost)
are saved. Then the function checks if the current state that was just popped is the goal, if it 
is, then the actions path is returned. If it is not the goal, then the function checks if the state
is already visited, if it is not, then the function gets a list of potential next states, these 
are then added to the stack with the addition of the extra actions. Finally, the state that was 
just checked out gets added to the visited list. Once this gets to the goal it returns the saved
actions list.

---------------------------Question 2: Breadth First Search------------------------------------
This question asks for an implementation of a breadth first search. This function returns a list 
of actions that can be used by pacman to find the dot inside the maze.
Bfs checks all of the adjacent states at the same level before moving to the next level.
This function works much like dfs except instead of using a stack, bfs is implemented using a queue.
This means the starting state is added to the queue, and then enters the loop which checks for the
goal, then if the state was visited before, then it pushes the next states and marks the current
one as visited.

---------------------------Question 3: Varying the Cost Function (Uniform Cost Search)----------
This question asks to implement a uniform cost search which works by choosing the cheapest route.
Much like question 2, this question works much like question 1 except the stack in dfs or the queue
in bfs is replaced with a priority queue.
This function works very similar to question 1 and question 2. The starting state is added to the 
queue, and then enters the loop which checks for the goal, then if the state was visited before, 
then it pushes the next states and marks the current one as visited. The main difference here is 
when the state gets pushed on to the priority queue. It pushed the state, actions, cost and now
the priority. The priority is made up of the cost to get the the current node + the cost to get
to the next node. This means the cheapest paths will be selected (front of the queue).

---------------------------Question 4: A* Search------------------------------------------------
This question asks to implement an A* search, this works a lot like ucs except instead of the
priority being just the cost, it now uses heuristics in addition to the cost to get there. 
Heuristics predict the number of steps are required to get to the goal.
This function works very similar to question 1 and question 2 andespecially question 3. T
he starting state is added to the queue, and then enters the loop which checks for the goal, then 
if the state was visited before, then it pushes the next states and marks the current one as 
visited. The main difference here is when the state gets pushed on to the priority queue. It 
pushed the state, actions, cost and now the priority. The priority is made up of the cost to 
get the the current node + the cost to get to the next node + the heuristic. 

---------------------------Question 5: Finding All the Corners-----------------------------------
This problem adds on to question 2, breadth first search by changing the CornersProblem to enable
the path finding algorithm to find all the corners in the pacman maze. This problem works by changing
the implementation of the state. Instead of only having the current location as the state, it has
the current location followed by the corners found ex ((4,5) [(1,1),(6,6)]). This means that 
the first breadth first search runs as usual until it finds the first corner. Then current 
location plus the list containing that corner gets added to the queue. This esentially wipes the 
graph as unvisited because pacmans new state is brand new and searching visited would find the 
first run with no corners found. This process continues until all 4 corners are added into the visited
corners list. When all 4 corners have been added to the list the goal state is reached which looks
to see if the length of the list equals 4.
Extra note: I had a lot of struggles with this problem. I first tried to initilize a visited list
belonging to "self" and adding each corner as it was visited. This had a fatal flaw in that each
corner was added to the list each time it was found with the regular bfs so it would reach a corner,
add it to the list, backtrack, visit, add, and so on. This meant only the last visited corner path
was returned. After this attempt I tried to save the directions in the getSuccessor method but didnt
get anywhere. When I was finally on the right path of saving the corners I changed my breadth first
search to use the indexes [0] and [1] for the state and list, but this ended up breaking question 3.
I finally realized that bfs had to remain the same and that all places I was putting the state[0] should
just be state and that I add the state and path into visited and the fringe.

---------------------------Question 6: Corners Problem: Heuristic----------------------------------
This problem asks us to create a heuristic for finding all the corners of the maze. This heuristics can
be passed into an A* search to get the optimal path. 
This function works by calculate the optimistic minimum path to reach all corners. I do this by first finding
the distance to the closest corner, then I say I am located there, I remove that corner from unvisited and 
again look for the next closest corner. I keep finding the closest corner and removing it from the unvisited 
list. Each time I find a the shortest path I add it to the heuristic that will be retuned. Since pacman can only
move in 4 degrees (NSEW), I use the manhattan distance function to find the smallest path between two nodes.
Since this function has simplified walls out of the equation, the returned path will always be less than or
equal to the actual path, depending if there are any walls in the way.

---------------------------Question 7: Eating All the Dots-----------------------------------------
This problem again asks us to create a heuristic, except this time, the goal is to eat all of the dots. 
This function works in a very similar way to question 6, but instead of keeping track of the unvisited corners it
keeps track of the uneaten food. This function starts at pacmans position and calculates the manhattan distance
to all the uneaten food nodes then picks the one with the shortest path, if that path is less than the heuristic, then
the heuristic gets updated, if it is not, then the distance is added to the heuristic. After this, the food node that
was just added gets removed from the food list (esentially being marked as visited) and becomes the next starting
node to search from. This process continues until all the food nodes have been visited (eaten).

---------------------------Question 8: Suboptimal Search-------------------------------------------
This problem throws out the optimal solution with a greedy algorithm that looks for the next closest food.
Luckily, we already have an algorithm that gives the smallest number of steps without looking at cost, bfs.
This problem just needs the goal state modified, which is the next closest food, or in other words, a location
with a square in it. I modified the goal state to return a true if it contains food and false if it does not.
I then added my bfs algorithm to the findPathToClosestDot which calls bfs from every location it stops, which
then searches for the next food, returns the path, and continues in that pattern until all food is eaten.