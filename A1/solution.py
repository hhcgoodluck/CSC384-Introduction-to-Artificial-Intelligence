#   You may only add standard python imports
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files
from typing import Callable, Union

import os                       # For time functions
import math                     # For infinity

from src import (
    # For search engine implementations
    SearchEngine, SearchNode, SearchStatistics,
    # For Sokoban-specific implementations
    SokobanState,
    sokoban_goal_state,
    UP, DOWN, LEFT, RIGHT,
    # You may further import any constants you may need.
    # See `search_constants.py`
)

# SOKOBAN HEURISTICS
def heur_alternate(state: 'SokobanState') -> float:
    """
    Returns a heuristic value with the goal of improving upon
    the flaws inherent to a heuristic that uses Manhattan distance
    and produce a more accurate estimate of the distance from the
    current state to the goal state.

    You must explain your heuristic via inline comments.

    :param state: A SokobanState object representing the current
                  state in a game of Sokoban.
    :return: An estimate of the distance from the current
             SokobanState to the goal state.

    raise NotImplementedError("You must implement heur_alternate.")
    """
    boxes, storage, obstacles = state.boxes, state.storage, state.obstacles
    width, height = state.width, state.height
    robots = state.robots

    # If all boxes are already placed, heuristic is zero.
    if boxes == storage: return 0.0

    # Only consider boxes not yet placed.
    unplaced_boxes = boxes - storage
    unplaced_storage = storage - boxes

    if not unplaced_storage: return 0.0

    # Boxes already correctly placed behave like static walls.
    placed_boxes = boxes & storage

    def is_static_block(x, y):
        """
        A static block is something that cannot move:
        - Wall (obstacle)
        - Boundary of board
        - A box already placed correctly
        """
        return (x, y) in obstacles or (x, y) in placed_boxes or \
            x < 0 or x >= width or y < 0 or y >= height

    # DEADLOCK DETECTION
    for bx, by in unplaced_boxes:
        # Check surrounding static directions
        up, down = is_static_block(bx, by - 1), is_static_block(bx, by + 1)
        left, right = is_static_block(bx - 1, by), is_static_block(bx + 1, by)

        # Corner Deadlock:
        # If a box is against a wall vertically AND horizontally,
        # and it's not on storage, it can never be moved.
        if (up or down) and (left or right):
            if (bx, by) not in storage:
                return math.inf

        # 2x2 Deadlock Pattern
        # If a 2x2 square region contains more boxes than storage cells,
        # and surrounded by static blocks, it becomes unsolvable.
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if (is_static_block(bx + dx, by) or (bx + dx, by) in boxes) and \
                    (is_static_block(bx, by + dy) or (bx, by + dy) in boxes) and \
                    (is_static_block(bx + dx, by + dy) or (bx + dx, by + dy) in boxes):

                cells = [(bx, by), (bx + dx, by), (bx, by + dy), (bx + dx, by + dy)]

                b_count, s_count = 0, 0
                for cell in cells:
                    if cell in boxes: b_count += 1
                    if cell in storage: s_count += 1

                # More boxes than storage means impossible configuration
                if b_count > s_count:
                    return math.inf

    # DISTANCE ESTIMATION
    # This is a computationally cheap approximation of optimal bipartite matching.

    # Perform sorted one-to-one pairing.
    # This approximates a minimum-cost matching and
    # prevents multiple boxes from being matched to the same storage location.

    # In contrast, a naive heuristic that matches each box to its
    # individually nearest storage may underestimate cost by
    # double-assigning storage positions.
    unplaced_boxes = sorted(list(unplaced_boxes))
    unplaced_storage = sorted(list(unplaced_storage))

    total_h = 0.0

    # Sum Manhattan distances for each paired box-storage pair.
    # Manhattan distance is admissible because a box must move
    # at least that many grid steps to reach its storage location, ignoring obstacles.
    for i in range(len(unplaced_boxes)):
        bx, by = unplaced_boxes[i]
        sx, sy = unplaced_storage[i]
        total_h += abs(bx - sx) + abs(by - sy)

    # ROBOT ACCESS COST

    # Boxes cannot move on their own, so at least one robot must first reach an adjacent cell to begin.
    # Therefore, can add a lower bound on the minimal cost required
    # for any robot to access at least one unplaced box.

    # Use Manhattan distance as a lower bound on robot movement,
    # this preserves admissibility since ignoring obstacles can only underestimate the true movement cost.

    if unplaced_boxes:
        min_r_dist = 999

        # To keep computation inexpensive, we can estimate this cost using a single
        # representative box (the first unplaced box), rather than minimizing over all box–robot pairs.

        # This provides a valid lower bound on the minimal robot-to-box access cost
        # while avoiding the higher computational cost of evaluating all combinations.
        tx, ty = unplaced_boxes[0]

        for rx, ry in robots:
            dist = abs(tx - rx) + abs(ty - ry)
            if dist < min_r_dist: min_r_dist = dist

        # subtracting 1 since the robot only needs to stand adjacent to the box.
        if min_r_dist > 1: total_h += (min_r_dist - 1)

    return float(total_h)

def heur_zero(state: 'SokobanState') -> float:
    """
    This function is used in A* to perform a uniform cost search
    by returning zero.

    :param state: A SokobanState object representing the current
                  state in a game of Sokoban.
    :return: The zero value.
    """
    return 0

def heur_manhattan_distance(state: 'SokobanState') -> float:
    """
    Returns an admissible - i.e. optimistic - heuristic by never
    overestimating the cost to transition from the current state to the goal state.
    The sum of the Manhattan distances between each box that has yet to be stored
    and the storage point nearest to it qualifies as such a heuristic.

    You may assume there are no obstacles on the grid when calculating distances.
    You must implement this function exactly as specified.

    :param state: A SokobanState object representing the current
                  state in a game of Sokoban.
    :return: An admissible estimate of the distance from the
             current SokobanState to the goal state.
    """
    total_dist = 0

    for box_pos in state.boxes:
        min_dist_for_box = math.inf

        for storage_position in state.storage:
            dist = abs(box_pos[0] - storage_position[0]) + abs(box_pos[1] - storage_position[1])

            if dist < min_dist_for_box:
                min_dist_for_box = dist

        if min_dist_for_box != math.inf:
            total_dist += min_dist_for_box

    return float(total_dist)

def fval_function(node: 'SearchNode', weight: float) -> float:
    """
    Returns the f-value of the state contained in node
    based on weight, to be used in Anytime Weighted A* search.

    Weighted A* evaluation function: f(n) = g(n) + weight * h(n)

    :param node: A SearchNode object containing a SokobanState object
    :param weight: The weight used in Anytime Weighted A* search.
    :return: The f-value of the state contained in node.

    raise NotImplementedError("You must implement fval_function.")
    """
    return node.gval + weight * node.hval

# SEARCH ALGORITHMS
def weighted_astar(
        initial_state: 'SokobanState',
        heur_fn: Callable,
        weight: float,
        timebound: int) -> tuple[Union['SokobanState', bool], 'SearchStatistics']:
    """
    Returns a tuple of the goal SokobanState and a SearchStatistics object
    by implementing weighted A* search as defined in the handout.

    If no goal state is found, returns a tuple of False and a SearchStatistics
    object.

    :param initial_state: The initial SokobanState of the game of Sokoban.
    :param heur_fn: The heuristic function used in weighted A* search.
    :param weight: The weight used in calculating the heuristic.
    :param timebound: The time bound used in weighted A* search, in seconds.
    :return: A tuple consisting of the goal SokobanState or False if such a state
             is not found, and a SearchStatistics object.

    raise NotImplementedError("You must implement weighted_astar.")
    """
    se = SearchEngine(strategy='custom')

    # Bind weight so the engine receives a function of one argument: f(node)
    wrapped_fval = (lambda node: fval_function(node, weight))

    se.init_search(
        init_state=initial_state,
        goal_fn=sokoban_goal_state,
        heur_fn=heur_fn,
        fval_fn=wrapped_fval
    )

    return se.search(timebound=timebound)

def iterative_astar( # uses f(n)
        initial_state: 'SokobanState',
        heur_fn: Callable,
        weight: float = 1,
        timebound: int = 5) -> tuple[Union['SokobanState', bool], 'SearchStatistics']:
    """
    Returns a tuple of the goal SokobanState and a SearchStatistics object
    by implementing realtime iterative A* search as defined in the handout.

    If no goal state is found, returns a tuple of False and a SearchStatistics
    object.

    Refer to test_alternate_fun in autograder.py to see how to initialize a search.

    :param initial_state: The initial SokobanState of the game of Sokoban.
    :param heur_fn: The heuristic function used in realtime iterative A* search.
    :param weight: The weight used in calculating the heuristic.
    :param timebound: The time bound used in realtime iterative A* search, in seconds.
    :return: A tuple consisting of the goal SokobanState or False if such a state
             is not found, and a SearchStatistics object.

    raise NotImplementedError("You must implement iterative_astar.")
    """
    start = os.times()[0]
    end = start + timebound

    best_state = False
    best_stats = None
    cost_bound = None
    curr_weight = weight

    while True:
        remaining = end - os.times()[0]
        if remaining <= 0:
            break

        se = SearchEngine(strategy='custom')
        wrapped_fval = (lambda node, w=curr_weight: fval_function(node, w))
        se.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval)
        result, stats = se.search(timebound=remaining, costbound=cost_bound)

        if best_stats is None: best_stats = stats

        if result and (best_state is False or result.gval < best_state.gval):
            best_state = result
            best_stats = stats
            best_g = best_state.gval
            cost_bound = (math.inf, math.inf, best_g)

        curr_weight = max(1, curr_weight * 0.5)

    return (best_state, best_stats) if best_state else (False, best_stats)

def iterative_gbfs( # uses h(n)
        initial_state: 'SokobanState',
        heur_fn: Callable,
        timebound: int = 5) -> tuple[Union['SokobanState', bool], 'SearchStatistics']:
    """
    Returns a tuple of the goal SokobanState and a SearchStatistics object
    by implementing iterative greedy best-first search as defined in the handout.

    :param initial_state: The initial SokobanState of the game of Sokoban.
    :param heur_fn: The heuristic function used in iterative greedy best-first search.
    :param timebound: The time bound used in iterative greedy best-first search, in seconds.
    :return: A tuple consisting of the goal SokobanState or False if such a state
             is not found, and a SearchStatistics object.

    raise NotImplementedError("You must implement iterative_gbfs.")
    """
    start = os.times()[0]
    end = start + timebound

    best_state = False
    best_stats = None
    cost_bound = None

    while True:
        remaining = end - os.times()[0]
        if remaining <= 0:
            break

        se = SearchEngine(strategy='best_first')
        se.init_search(initial_state, sokoban_goal_state, heur_fn)
        result, stats = se.search(timebound=remaining, costbound=cost_bound)

        if best_stats is None: best_stats = stats

        if result and (best_state is False or result.gval < best_state.gval):
            best_state = result
            best_stats = stats
            best_g = best_state.gval
            cost_bound = (best_g, math.inf, math.inf)

    return (best_state, best_stats) if best_state else (False, best_stats)