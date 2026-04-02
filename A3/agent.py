from typing import Callable, Optional

# These functions are imported for you to use
# in your implementation.
from src import (
    find_lines,
    get_possible_moves,
    get_score,
    play_move,
    eprint      # for debugging
)

# Use this global variable for state caching.
# You may find that it's useful to use the following
# information to form a key into the
#
#       (board, player_to_move, limit, node_type)
#
state_cache = {}


###############################################################################
############################# VALUE FUNCTIONS #################################
###############################################################################
def compute_utility(board: tuple[tuple[int, ...], ...], color: int) -> int:
    """
    Return the utility value of the given board for the given player color.

    :param board: a board representing the current state of an Othello game
    :param color: the color of the player. 1 for dark, 2 for light.

    :return: the utility of the given board for the given player color.

    raise RuntimeError("Method not implemented")  # Replace this line!
    """
    dark, light = get_score(board)

    if color == 1:
        return dark - light
    else:
        return light - dark


# Heuristic description:
# This heuristic prioritizes corner ownership, mobility,
# and avoiding dangerous squares adjacent to empty corners.
# It also changes weights across the opening, mid-game,
# and end-game: mobility is emphasized early,
# while disk difference becomes more important late in the game.

def compute_heuristic(board: tuple[tuple[int, ...], ...], color: int) -> int:
    """
    Return the heuristic value of the given board for the given player color.

    :param board: a board representing the current state of an Othello game
    :param color: the color of the player. 1 for dark, 2 for light.

    :return: the heuristic value of the given board for the given player color.

    raise RuntimeError("Method not implemented")  # Replace this line!

    Heuristic for Othello:
    - prefer corners because they are stable
    - prefer positions with higher mobility
    - avoid squares adjacent to empty corners
    - use different weights in opening, mid-game, and end-game
    """
    opponent_color = 3 - color
    n = len(board)

    # Count occupied squares to determine game stage
    occupied = 0
    for row in board:
        for cell in row:
            if cell != 0:
                occupied += 1

    total_squares = n * n
    progress = occupied / total_squares

    # 1. Piece difference
    piece_score = compute_utility(board, color)

    # 2. Mobility
    my_moves = len(get_possible_moves(board, color))
    opp_moves = len(get_possible_moves(board, opponent_color))
    mobility_score = my_moves - opp_moves

    # 3. Corner control
    corners = [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]
    corner_score = 0
    for r, c in corners:
        if board[r][c] == color:
            corner_score += 1
        elif board[r][c] == opponent_color:
            corner_score -= 1

    # 4. Penalty for squares adjacent to empty corners
    danger_score = 0
    danger_map = {
        (0, 0): [(0, 1), (1, 0), (1, 1)],
        (0, n - 1): [(0, n - 2), (1, n - 1), (1, n - 2)],
        (n - 1, 0): [(n - 2, 0), (n - 1, 1), (n - 2, 1)],
        (n - 1, n - 1): [(n - 2, n - 1), (n - 1, n - 2), (n - 2, n - 2)],
    }

    for corner, danger_squares in danger_map.items():
        cr, cc = corner
        if board[cr][cc] == 0:
            for r, c in danger_squares:
                if board[r][c] == color:
                    danger_score -= 1
                elif board[r][c] == opponent_color:
                    danger_score += 1

    # Phase-based weights
    if progress < 0.30:
        # Opening: mobility matters most, piece count matters least
        return 20 * corner_score + 8 * mobility_score + 4 * danger_score + 0 * piece_score
    elif progress < 0.75:
        # Mid-game: balanced
        return 25 * corner_score + 6 * mobility_score + 4 * danger_score + 1 * piece_score
    else:
        # End-game: actual disk difference matters much more
        return 25 * corner_score + 3 * mobility_score + 2 * danger_score + 6 * piece_score

###############################################################################
####################### ALPHA-BETA PRUNING FUNCTIONS ##########################
###############################################################################
def alphabeta_min_node(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        alpha: int,
        beta: int,
        limit: int,
        caching: int = 0,
        ordering: int = 0) -> tuple[Optional[tuple[int, int]], int]:
    """
    Return a tuple of the move that yields the *lowest* possible utility
    and the *lowest* possible utility itself for the given board, color,
    limit, value_fn to determine utility and alpha, beta to prune.
    Optionally use state caching and node ordering.

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param alpha: the alpha parameter, used in pruning
    :param beta: the beta parameter, used in pruning
    :param limit: the depth limit of the alpha-beta search
    :param caching: whether to use state caching
                    if 1, use state caching
                    if 0, do not use state caching
    :param ordering: whether to order moves during move selection

    :return: a tuple (None|(i,j), utility) of the next move to be
             taken, and the utility value associated with it

    raise RuntimeError("Method not implemented")  # Replace this line!
    """
    cache_key = (board, color, limit, "ab_min")
    if caching and cache_key in state_cache:
        return state_cache[cache_key]

    opponent_color = 3 - color
    moves = get_possible_moves(board, opponent_color)

    if not moves or limit == 0:
        result = (None, value_fn(board, color))
        if caching:
            state_cache[cache_key] = result
        return result

    next_limit = limit if limit == -1 else limit - 1
    best_move = None
    best_utility = float("inf")

    move_list = []
    for move in moves:
        new_board = play_move(board, opponent_color, move[0], move[1])
        move_list.append((move, new_board))

    if ordering:
        move_list.sort(key=lambda pair: value_fn(pair[1], color))

    for move, new_board in move_list:
        _, utility = alphabeta_max_node(
            value_fn,
            new_board,
            color,
            alpha,
            beta,
            next_limit,
            caching,
            ordering
        )

        if utility < best_utility:
            best_utility = utility
            best_move = move

        beta = min(beta, best_utility)
        if beta <= alpha:
            break

    result = (best_move, best_utility)
    if caching:
        state_cache[cache_key] = result
    return result


def alphabeta_max_node(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        alpha: int,
        beta: int,
        limit: int,
        caching: int = 0,
        ordering: int = 0) -> tuple[Optional[tuple[int, int]], int]:
    """
    Return a tuple of the move that yields the *highest* possible utility
    and the *highest* possible utility itself for the given board, color,
    limit, value_fn to determine utility and alpha, beta to prune.
    Optionally use state caching and node ordering.

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param alpha: the alpha parameter, used in pruning
    :param beta: the beta parameter, used in pruning
    :param limit: the depth limit of the alpha-beta search
    :param caching: whether to use state caching
                    if 1, use state caching
                    if 0, do not use state caching
    :param ordering: whether to order moves during move selection

    :return: a tuple (None|(i,j), utility) of the next move to be
             taken, and the utility value associated with it

    raise RuntimeError("Method not implemented")  # Replace this line!
    """
    cache_key = (board, color, limit, "ab_max")
    if caching and cache_key in state_cache:
        return state_cache[cache_key]

    moves = get_possible_moves(board, color)

    if not moves or limit == 0:
        result = (None, value_fn(board, color))
        if caching:
            state_cache[cache_key] = result
        return result

    next_limit = limit if limit == -1 else limit - 1
    best_move = None
    best_utility = float("-inf")

    move_list = []
    for move in moves:
        new_board = play_move(board, color, move[0], move[1])
        move_list.append((move, new_board))

    if ordering:
        move_list.sort(key=lambda pair: value_fn(pair[1], color), reverse=True)

    for move, new_board in move_list:
        _, utility = alphabeta_min_node(
            value_fn,
            new_board,
            color,
            alpha,
            beta,
            next_limit,
            caching,
            ordering
        )

        if utility > best_utility:
            best_utility = utility
            best_move = move

        alpha = max(alpha, best_utility)
        if beta <= alpha:
            break

    result = (best_move, best_utility)
    if caching:
        state_cache[cache_key] = result
    return result


def select_move_alphabeta(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        limit: int = -1,
        caching: int = 0,
        ordering: int = 0) -> Optional[tuple[int, int]]:
    """
    Return the next move determined by alpha-beta pruning in a game of Othello
    defined by the given board, player color, depth limit, and use of caching
    and node ordering. Use value_fn to determine utility values in subroutines.

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param limit: the depth limit of the alpha-beta search
    :param caching: whether to use state caching
                    if 1, use state caching
                    if 0, do not use state caching
    :param ordering: whether to order moves during move selection

    :return: a tuple (i, j) of the next move to be taken, or None

    raise RuntimeError("Method not implemented")  # Replace this line!
    """
    move, _ = alphabeta_max_node(
        value_fn,
        board,
        color,
        float("-inf"),
        float("inf"),
        limit,
        caching,
        ordering
    )
    return move

###############################################################################
############################# MINIMAX FUNCTIONS ###############################
###############################################################################
def minimax_min_node(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        limit: int,
        caching: int = 0) -> tuple[Optional[tuple[int, int]], int]:
    """
    Return a tuple of the move that yields the lowest possible utility
    and the lowest possible utility itself for the given board, color,
    limit, using value_fn to determine utility. Optionally use state caching
    and node ordering.

    The algorithm is outlined as follows:
        1. Get all allowed moves
        2. Check if we are at a terminal state
        3. If not, minimize over the set of max utility values for each possible move

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param limit: the depth limit of the Minimax search
    :param caching: whether to use state caching in Minimax
                    if 1, use state caching
                    if 0, do not use state caching

    :return: a tuple (None|(i,j), utility) of the next move to be
             taken, and the utility value associated with it

    raise NotImplementedError("minimax_min_node is not implemented")
    """
    cache_key = (board, color, limit, "min")
    if caching and cache_key in state_cache:
        return state_cache[cache_key]

    opponent_color = 3 - color
    moves = get_possible_moves(board, opponent_color)

    if not moves or limit == 0:
        result = (None, value_fn(board, color))
        if caching:
            state_cache[cache_key] = result
        return result

    best_move = None
    best_utility = float("inf")
    next_limit = limit if limit == -1 else limit - 1

    for move in moves:
        new_board = play_move(board, opponent_color, move[0], move[1])
        _, utility = minimax_max_node(
            value_fn,
            new_board,
            color,
            next_limit,
            caching
        )

        if utility < best_utility:
            best_utility = utility
            best_move = move

    result = (best_move, best_utility)
    if caching:
        state_cache[cache_key] = result
    return result


def minimax_max_node(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        limit: int,
        caching: int = 0) -> tuple[Optional[tuple[int, int]], int]:
    """
    Return a tuple of the move that yields the highest possible utility
    and the highest possible utility itself for the given board, color,
    limit, using value_fn to determine utility. Optionally use state caching
    and node ordering.

    The algorithm is outlined as follows:
        1. Get all allowed moves
        2. Check if we are at a terminal state
        3. If not, maximize over the set of min utility values for each possible move

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param limit: the depth limit of the Minimax search
    :param caching: whether to use state caching in Minimax
                    if 1, use state caching
                    if 0, do not use state caching

    :return: a tuple (None|(i,j), utility) of the next move to be
             taken, and the utility value associated with it

    raise NotImplementedError("minimax_max_node is not implemented")
    """
    cache_key = (board, color, limit, "max")
    if caching and cache_key in state_cache:
        return state_cache[cache_key]

    moves = get_possible_moves(board, color)

    if not moves or limit == 0:
        result = (None, value_fn(board, color))
        if caching:
            state_cache[cache_key] = result
        return result

    best_move = None
    best_utility = float("-inf")
    next_limit = limit if limit == -1 else limit - 1

    for move in moves:
        new_board = play_move(board, color, move[0], move[1])
        _, utility = minimax_min_node(
            value_fn,
            new_board,
            color,
            next_limit,
            caching
        )

        if utility > best_utility:
            best_utility = utility
            best_move = move

    result = (best_move, best_utility)
    if caching:
        state_cache[cache_key] = result
    return result


def select_move_minimax(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        limit: int,
        caching: int = 0) -> Optional[tuple[int, int]]:
    """
    Return the next move determined by Minimax in a game of Othello
    defined by the given board, player color, depth limit, and use of caching.
    Uses value_fn to determine utility values in subroutines.

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param limit: the depth limit of the Minimax search
    :param caching: whether to use state caching
                    if 1, use state caching
                    if 0, do not use state caching

    :return: a tuple (i, j) of the next move to be taken, or None

    raise NotImplementedError("select_move_minimax is not implemented")
    """
    move, _ = minimax_max_node(value_fn, board, color, limit, caching)
    return move


###############################################################################
############################### ENTRY-POINT ###################################
###############################################################################
def run_ai():
    """
    Communicate with the game manager to simulate a player in a game
    of Othello. Accepts input from stdin to determine:
        * color    - 1 for dark, 2 for light
        * limit    - the depth limit
        * minimax  - 1 to run minimax, otherwise run alpha-beta
        * caching  - 1 to run with caching, otherwise run without it
        * ordering - 1 to run alpha-beta with node ordering,
                     otherwise run without it.

    Use `compute_utility` as the value function by default.
    """
    print("Othello AI")  # First line is the name of this AI
    color, limit, minimax, caching, ordering = map(int, input().split(","))

    eprint("Running MINIMAX") if minimax else eprint("Running ALPHA-BETA")
    eprint("State Caching is ON") if caching else eprint("State Caching is OFF")
    eprint("Node Ordering is ON") if ordering else eprint("Node Ordering is OFF")
    eprint("Depth Limit is ", limit) if limit >= 0 else eprint("Depth Limit is OFF")

    while True:
        # Read the current state of the game as yielded by the game manager.
        # Consists of a string of the form:
        #
        #       (SCORE|FINAL) \d+ \d+    , e.g. SCORE 9 7
        #
        # The first string is the state of the game:
        #   * SCORE indicates that the game is still active.
        #   * FINAL indicates that the game is over.
        #
        # The first digit is the score for player 1 (the dark player.)
        #
        # The second digit is the score for player 2 (the light player.)
        status, _, _ = input().strip().split()

        if status == "FINAL":
            break
        else:
            # Read the current board represented as a tuple of tuples, where
            # nested tuples represent rows of the board. For example:
            #
            #   ((0, 0, 0, 0),
            #    (0, 2, 1, 0),
            #    (0, 1, 2, 0),
            #    (0, 0, 0, 0))
            #
            # where
            #
            #   * 0 - an empty square on the board
            #   * 1 - a piece played by player 1, or the dark player.
            #   * 2 - a piece played by player 2, or the light player.
            board = eval(input())

            if (minimax == 1):
                i, j = select_move_minimax(
                    compute_utility,  # compute_heuristic
                    board,
                    color,
                    limit,
                    caching
                )
            else:
                i, j = select_move_alphabeta(
                    compute_utility,  # compute_heuristic
                    board,
                    color,
                    limit,
                    caching,
                    ordering
                )

            print("{} {}".format(i, j))


if __name__ == "__main__":
    run_ai()
