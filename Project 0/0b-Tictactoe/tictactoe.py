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
    count_of_x = 0
    count_of_o = 0
    for a_row in board:
        for a_cell in a_row:
            if a_cell == X:
                count_of_x = count_of_x + 1
            if a_cell == O:
                count_of_o = count_of_o + 1
    if count_of_x == count_of_o:
        return X
    else:
        return O


def actions(board):
    moves = set()
    for p in range(3):
        for q in range(3):
            if board[p][q] == EMPTY:
                moves.add((p, q))
    return moves


def result(board, action):
    updated_board = [a_row[:] for a_row in board]
    r, s = action
    updated_board[r][s] = player(board)
    return updated_board


def winner(board):
    for a_row in board:
        if a_row[0] == a_row[1] == a_row[2] and a_row[0] is not None:
            return a_row[0]

    for a_column in range(3):
        if board[0][a_column] == board[1][a_column] == board[2][a_column] and board[0][a_column] is not None:
            return board[0][a_column]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None


def terminal(board):
    if winner(board) is not None:
        return True
    for a_row in board:
        for a_cell in a_row:
            if a_cell is EMPTY:
                return False
    return True


def utility(board):
    p = winner(board)
    if p == X:
        return  1
    elif p == 0:
        return -1
    else:
        return 0


def minimax(board):
    if player(board) == X:
        high_score = -100
        accurate_move = None
        for an_action in actions(board):
            score = min_value(result(board, an_action))
            if score > high_score:
                high_score = score
                accurate_move = an_action
        return accurate_move

    else:
        high_score = 100
        accurate_move = None
        for an_action in actions(board):
            score = max_value(result(board, an_action))
            if score < high_score:
                high_score = score
                accurate_move = an_action
        return accurate_move


def max_value(board):
    if terminal(board):
        return utility(board)
    best = -100
    for an_action in actions(board):
        score = min_value(result(board, an_action))
        if score > best:
            best = score
    return best


def min_value(board):
    if terminal(board):
        return utility(board)
    best = 100
    for an_action in actions(board):
        score = max_value(result(board, an_action))
        if score < best:
            best = score
    return best

