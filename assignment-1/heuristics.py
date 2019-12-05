# heuristics.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This class contains heuristics which are used for the search procedures that
    you write in search_strategies.py.

    The first part of the file contains heuristics to be used with the algorithms
    that you will write in search_strategies.py.

    In the second part you will write a heuristic for Q4 to be used with a
    MultiplePositionSearchProblem.
"""

#-------------------------------------------------------------------------------
# A set of heuristics which are used with a PositionSearchProblem
# You do not need to modify any of these.
#-------------------------------------------------------------------------------

def null_heuristic(pos, problem):
    """ The null heuristic. It is fast but uninformative. It always returns 0.
        (State, SearchProblem) -> int
    """
    return 0

def manhattan_heuristic(pos, problem):
    """ The Manhattan distance heuristic for a PositionSearchProblem.
      ((int, int), PositionSearchProblem) -> int
    """
    return abs(pos[0] - problem.goal_pos[0]) + abs(pos[1] - problem.goal_pos[1])

def euclidean_heuristic(pos, problem):
    """ The Euclidean distance heuristic for a PositionSearchProblem
        ((int, int), PositionSearchProblem) -> float
    """
    return ((pos[0] - problem.goal_pos[0]) ** 2 + (pos[1] - problem.goal_pos[1]) ** 2) ** 0.5

# Abbreviations
null = null_heuristic
manhattan = manhattan_heuristic
euclidean = euclidean_heuristic

#-------------------------------------------------------------------------------
# You have to implement the following heuristics for Q4 of the assignment.
# It is used with a MultiplePositionSearchProblem
#-------------------------------------------------------------------------------

# You can make helper functions here, if you need them


def bird_counting_heuristic(state, problem) :
    """ Return the number of yellow birds still to be captured.

        (((int, int), ((int, int))), MultiplePositionSearchProblem) -> int

        By Jeff Yuanbo Han (u6617017), 2018-03-29.
    """
    return len(state[1])


bch = bird_counting_heuristic


def every_bird_heuristic(state, problem):
    """ Find a minimum spanning tree (MST) among all the remaining birds by Prime's algorithm.
        Return the sum of the edges costs in the MST.

        (((int, int), ((int, int))), MultiplePositionSearchProblem) -> int

        By Jeff Yuanbo Han (u6617017), 2018-03-29.
    """
    position, yellow_birds = state
    vertices = {position} | set(yellow_birds)  # All the remaining birds (both red and yellow).
    included = {position}  # The vertices already included in the MST.
    mst = 0  # The sum of the edge costs in the MST.

    while included != vertices:
        next_growth = (None, float('inf'))  # The next vertex and edge (cost) to be included in the MST.
        # Choose the closest (to the current tree) unvisited vertex.
        for vertex1 in included:
            for vertex2 in vertices-included:
                dist = problem.maze_distance(vertex1, vertex2)
                if dist < next_growth[1]:
                    next_growth = (vertex2, dist)
        mst += next_growth[1]
        included.add(next_growth[0])

    return mst


every_bird = every_bird_heuristic
