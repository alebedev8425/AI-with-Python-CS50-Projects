"""
Tic Tac Toe Player
"""

import math

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

    xCount = sum(row.count(X) for row in board)
    oCount = sum(row.count(O) for row in board)

    if xCount > oCount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")

    newBoard = []
    for row in board:
        newRow = row.copy()
        newBoard.append(newRow)
    newBoard[i][j] = player(board)
    return newBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    currentPlayer = player(board)
    if currentPlayer == X:
        bestScore = float('-inf')
        bestAction = None
        for action in actions(board):
            nextMoveScore = minValue(result(board, action))
            if nextMoveScore > bestScore:
                bestScore = nextMoveScore
                bestAction = action
        return bestAction
    else:
        bestScore = float('inf')
        bestAction = None
        for action in actions(board):
            nextMoveScore = maxValue(result(board, action))
            if nextMoveScore < bestScore:
                bestScore = nextMoveScore
                bestAction = action
        return bestAction



def minValue(board):
    if terminal(board):
        return utility(board)

    value = float('inf')
    for action in actions(board):
        value = min(value, maxValue(result(board, action)))

    return value

def maxValue(board):
    if terminal(board):
        return utility(board)

    value = float('-inf')
    for action in actions(board):
        value = max(value, minValue(result(board, action)))
    return value