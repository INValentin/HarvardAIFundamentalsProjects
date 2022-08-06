"""
Tic Tac Toe Player
"""

from copy import deepcopy

from more_itertools import flatten

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
    num_x = 0
    num_o = 0

    for row in board:
        num_x += row.count(X)
        num_o += row.count(O)

    return X if num_x == num_o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i, row in enumerate(board):
        for j in range(3):
            if row[j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if board[i][j] != EMPTY:
        raise Exception("Invalid board action!", (i, j))

    new_board = deepcopy(board)
    new_board[i][j] = player(new_board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    board_flat = list(flatten(board))

    for i in range(3):
        if all(cell == X for cell in board[i]):
            return X
        if all(cell == O for cell in board[i]):
            return O

    for i in range(3):
        if board_flat[i] == board_flat[i+3] == board_flat[i + 6] == X:
            return X
        if board_flat[i] == board_flat[i+3] == board_flat[i + 6] == O:
            return O

    if all(board_flat[i*2] == X for i in range(0, 5, 2)):
        return X

    if all(board_flat[i*2] == X for i in range(1, 4)):
        return X

    if all(board_flat[i*2] == O for i in range(0, 5, 2)):
        return O

    if all(board_flat[i*2] == O for i in range(1, 4)):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for row in board:
        if any(cell == EMPTY for cell in row):
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player = winner(board)

    if player == X:
        return 1
    elif player == O:
        return -1

    return 0


def minimax(board, depth = 0):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        if depth == 0:
            return None
        return utility(board)
        

    x_turn = player(board) == X
    best_action = None
    best_score = -10000 if x_turn else 10000

    for action in actions(board):
        new_board = result(board, action)
        result_value = minimax(new_board,  depth+ 1)

        if x_turn:
            new_best_score = max(best_score, result_value)
            if new_best_score > best_score:
                best_score = new_best_score
                best_action = action
        else:
            new_best_score = min(best_score, result_value)
            if new_best_score < best_score:
                best_score = new_best_score
                best_action = action
                
    return best_action if depth == 0 else best_score
