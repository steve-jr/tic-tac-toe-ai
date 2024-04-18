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