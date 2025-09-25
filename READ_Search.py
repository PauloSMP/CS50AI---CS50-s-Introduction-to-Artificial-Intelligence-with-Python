#AI is a broad field that encompasses various subfields and techniques. Here are some of the key areas within AI:
#Search
#Knowledge
#Uncertainty
#Optimization
#Machine Learning

#Machine learning is very important subfield of AI that can also be divided into several categories, from which we will focus on the following techniques/areas:
#Artificial Neural Networks (ANNs)
#Language Processing

####Section 1: Search####

#Agent - A entity that perceives its enviroment and acts upon it to  achieve a goal.

#State - A representation of the current situation of the agent in its environment.

#Initial State - The state in which the agent starts its operation.

#Actions - The possible operations that the agent can perform in its environment.
#Actions(s) - The set of all possible actions that can be performed in state s.

#Transition Model - A description of how the state changes when an action is performed.
#Result(s, a) - The state that results from performing action a in state s.

#State Space - The set of all possible states that the agent can reach from the initial state by any sequence of actions.

#Goal Test - A state that satisfies the goal of the agent. Allows the agent to determine if it has achieved its goal.

#Path Cost Function - A numerical value that represents the cost of performing a sequence of actions to reach a state. It is used to evaluate the efficiency of a path.

#Optimal Solution - A solution that minimizes the path cost function. It is the most efficient way to achieve the goal.

#Node: A data structure that keeps track of:
#- State: The current state of the agent.
#- Parent: The node that generated this node.
#- Action: The action that was performed to reach this state.
#- Path Cost: The cost of the path from the initial state to this state.


#######################################################UNINFORMED SEARCH ALGORITHMS#######################################################
#Dont use any information about the problem domain to guide the search.


#Approach to Search (Depth-First-Search):
##### - Allways explore the deepest node in the frontier first.

# Start with a frontier that contains the initial state.
# Start with an empty explored set.
# Repeat until the frontier(set of nodes available for expansion) is empty:
# - If the frontier is empty, then no solution exists. Nothing left to explore.
# - Remove a node from the frontier. (Use stack data structure, fist-in-last-out)
# - If the node contains the goal state, then return the solution.
# - Add the node to the explored set (to avoid re-exploring it).
# - Expand the node, add resulting nodes to the frontier if they are not alread in the frontiert or explored set.


#Approach to Search (Breadth-First-Search):
### - Allways explore the shallowest node in the frontier first. Kinda of at the same time, different from DFS that will explore one path until exhausted.
#Insted of using a stack, use a queue data structure (first-in-first-out).
#######################################################UNINFORMED SEARCH ALGORITHMS#######################################################


############################################################INFORMED SEARCH ALGORITHMS#######################################################
#search strategy that uses problem-specific knowledge to find solutions more efficiently.

#Greedy Best-First Search:
#Searches algorhm that expands the node that is closest to the goal, as estiimated by a heuristic function h(n).
#Heuristic function h(n) - A function that estimates the cost of the cheapest path from node n to the goal. "How close is the node to the goal?"

#A heuristic funciton that is commonly used is the Manhattan distance. Calculates the distance between two points in a grid by summing the absolute differences of their coordinates.

#Note: This algorithm does not guarantee the optimal solution, as it may get sttuck in a local minimum.
#Note: That is why is called "Greedy", because it only looks at the immediate cost of the next step, not the overall cost of the path.


#A* Search:
#Search algorhtm that expands the node with lowest value of g(n) + h(n).
#g(n) - The cost to reach node.
#h(n) - The estimated cost to the goal.

#In conclusion it calculates how many steps it takes to rach the actual node and how many steps are left to reach the goal.

#The heyristic function is the key to the efficiency of A* search. It must be designed to ensure that:
# h(n) is admissible (never overestmates the true cost) and
# h(n) is consistent (for every node n and sucessor n' with step cost c,h(n) <= (h(n') + c)


#######################################################Adversarial Search Algorithms#######################################################
#Adversarial search is a type of search that is used in games and other situations where two or more agents are competing against each other.

#Minimax Algorithm:
#A search algorithm that is used to find the optimal move in a two-player game.

# -1 represents the worst case for the player, 1 represents the best case for the player. (O)
# 0 represents a draw.
# 1 represents the best case for the player, -1 represents the worst case for the player. (X)

#In tic-tac-toe game exaple:
#Max(X) aims to maximize the score.
#Min(O) aims to minimize the score.

#Game:
# S0 - Initial state of the game.
# Player(s): return which player to move in state s.
# Actions(s): returns legal moves for the player in state s.
# Result(s,a): returns the state after action a taken in state s.
# Terminal(s): checks if the state s is a terminal state (win, lose, draw).
# Utility(s): final numerical value for terminal state s.

# Given a state s:
# - Max picks action a in Actions(s) that produces highest value of Min-Value(Result(s, a)).
# - Min picks action a in Actions(s) that produces lowest value of Max-Value(Result(s, a)).
#
# (This function is for maximizing player, usually called Max or X)
#Function Max-Value(state):
# if terminal(state):
#     return Utility(state)
#
# v = -infinity
# for action in Actions(state):
# v = Max(v, Min-Value(Result(state, action)))
# return v
# (For minimizing player, usually called Min or O)
#Function Min-Value(state):
# if terminal(state):
#     return Utility(state)
# v = +infinity
# for action in Actions(state):
#     v = Min(v, Max-Value(Result(state, action)))
# return v

#If the game is simples, you can use the Minimax algorithm to find the optimal move for the player.
# If the game is more complex, we need to optimize the search process using special techniques.

#One of the most common techniques is Alpha-Beta Pruning:
#Alpha-Beta Pruning:
#A technique that reduces the number of nodes that are evaluated in the Minimax algorithm by eliminating branches that cannot possibly influence the final decision.
#Alpha-Beta Pruning works by keeping track of two values, alpha and beta, which represent the minimum score that the maximizing player is assured of and the maximum score that the minimizing player is assured of, respectively.
#If the value of a node is worse than alpha or beta, then the node is pruned and not evaluated further.


#Another aproach/feature to classical MiniMax algorith is the Depth-Limited Minimax:
#Depth-Limited Minimax:
#A variation of the Minimax algorithm that limits the depth of the search tree to a specified depth.
#This is useful for games with a large search space, as it allows the algorithm to find a good move without evaluating the entire search tree.
#For example it will look further only x number of moves ahead, instead of looking at the entire game tree.

#For this approach we need a evaluation function that estimates the value of a non-terminal state.