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