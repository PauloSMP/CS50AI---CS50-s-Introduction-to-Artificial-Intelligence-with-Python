"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                countX += 1
            if board[row][col] == O:
                countO += 1
    
    if countX > countO:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_valid_actions = set()
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                all_valid_actions.add((row, col))
    return all_valid_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception ("Invalid Action")

    row, col = action
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return board_copy

def check_row(board, player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True 
    return False

def check_col(board,player):
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False

def check_diagonal(board,player):
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_row(board, X) or check_col(board, X) or check_diagonal(board,X):
        return X
    elif check_row(board, O) or check_col(board, O) or check_diagonal(board, O):
        return O
    else:
        return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True
    if winner(board) == O:
        return True
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def max_value(board, alpha, beta):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board,action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def min_value(board, alpha, beta):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board,action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    current_player = player(board)
    best_action = None
    
    #Case of X (max-player)
    if current_player == X:
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf
        for action in actions(board):
            value = min_value(result(board, action), alpha ,beta)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)
        #plays = []
    #Loop through all actions
        #for action in actions(board):
            #Add in plays a tupple with min value and action that results to its value
        #    plays.append([min_value(result(board, action)), action])
        #Reverse sort the plays list and get the action that should be played.
        #This sorted list will give us the result of highest value first and we will also take the action that results to it.
        #return sorted(plays, key=lambda X: X[0], reverse=True)[0][1]
    
    #Case of O (min-player)
    if current_player == O:
        best_value = math.inf
        alpha = -math.inf
        beta = math.inf
        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)
            if value < best_value:
                best_value = value
                best_action = action
            beta = min(beta, best_value)
    #elif player(board) == O:
        #plays = []
        #for action in actions(board):
        #    plays.append([max_value(result(board, action)), action])
        #return sorted(plays, key=lambda X: X[0])[0][1]
        
        
    return best_action
