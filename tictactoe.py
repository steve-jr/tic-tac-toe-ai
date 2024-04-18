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

    Args:
    board (list of list): Current board state

    Returns:
    str: 'X' or 'O' depending on whose turn it is

    """
    # Count moves by X and O
    x_moves = sum(row.count('X') for row in board)
    o_moves = sum(row.count('O') for row in board)
    return 'O' if x_moves > o_moves else 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    Args:
    board (list of list): Current board state

    Returns:
    set: Set of tuples representing all empty positions where a move can be made
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    Args:
    board (list of list): Current board state
    action (tuple): A tuple (i, j) indicating the next move

    Returns:
    list of list: New board state after the move
    """
    import copy
    new_board = copy.deepcopy(board)
    i, j = action
    turn = player(board)
    new_board[i][j] = turn
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.

    Args:
    board (list of list): Current board state

    Returns:
    str: 'X' if X wins, 'O' if O wins, None otherwise
    """
    # Check rows, columns, and diagonals for a winner
    lines = board + [list(x) for x in zip(*board)] + [[board[i][i] for i in range(3)],
                                                      [board[i][2 - i] for i in range(3)]]
    for line in lines:
        if line == ['X', 'X', 'X']:
            return 'X'
        if line == ['O', 'O', 'O']:
            return 'O'
    return None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.

    Args:
    board (list of list): Current board state

    Returns:
    int: The utility value of the board
    """
    win = winner(board)
    if win == 'X':
        return 1
    elif win == 'O':
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    Args:
    board (list of list): Current board state

    Returns:
    tuple: The best move (i, j) for the current player
    """
    if terminal(board):
        return None
    turn = player(board)

    # Choose the action that maximizes (for 'X') or minimizes (for 'O') the utility value of the result board
    if turn == 'X':
        # For X, find the action leading to the maximum value obtainable.
        return max((min_value(result(board, action)), action) for action in actions(board))[1]
    else:
        # For O, find the action leading to the minimum value obtainable.
        return min((max_value(result(board, action)), action) for action in actions(board))[1]


def max_value(board):
    """
    Calculate the maximum utility value that the maximizing player can obtain from the current board state.

    Args:
    board (list of list): Current board state

    Returns:
    int: The maximum utility value
    """
    if terminal(board):
        return utility(board)
    v = float('-inf') # Initialize v to the lowest possible value
    for action in actions(board):
        # Recursively calculate the value of the board resulting from taking each possible action
        # and take the maximum of these values.
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    """
    Calculate the minimum utility value that the minimizing player can obtain from the current board state.

    Args:
    board (list of list): Current board state

    Returns:
    int: The minimum utility value
    """
    if terminal(board):
        return utility(board)
    v = float('inf') # Initialize v to the highest possible value
    for action in actions(board):
        # Recursively calculate the value of the board resulting from taking each possible action
        # and take the minimum of these values.
        v = min(v, max_value(result(board, action)))
    return v


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    Args:
    board (list of list): Current board state

    Returns:
    bool: True if the game is over (either a win or a tie), False otherwise
    """
    if winner(board) is not None:
        return True
    return all(cell != EMPTY for row in board for cell in row)