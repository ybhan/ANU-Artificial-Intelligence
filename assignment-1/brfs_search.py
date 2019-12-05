"""
    Enter your details below:

    Name: Jeff Yuanbo Han
    Student ID: u6617017
    Email: u6617017@anu.edu.au
"""

from frontiers import Queue
from search_strategies import SearchNode


def solve(problem):
    """ Return a list of directions. See handout for more details. """

    # The frontier is a Queue (defined in frontiers.py), for its FIFO queuing policy.
    frontier = Queue()
    # Use SearchNode (defined in search_strategies.py) as the class of elements in frontier, and initialize frontier.
    node = SearchNode(problem.get_initial_state())
    frontier.push(node)

    explored = []  # The closed list (of states already explored).

    while not frontier.is_empty():
        # Check the first node in frontier.
        node = frontier.pop()
        if problem.goal_test(node.state):
            break

        # Expand this node if it is not the goal.
        for successor, action, cost in problem.get_successors(node.state):
            # Avoid revisiting the explored states.
            if successor in explored:
                continue
            else:
                explored.append(successor)

            # Add the successor node to frontier.
            frontier.push(
                SearchNode(state=successor,
                           action=action,
                           path_cost=node.path_cost + cost,
                           parent=node,
                           depth=node.depth + 1))

    # Obtain the path from start state to the goal, by the attribute parent of SearchNode.
    path = []
    while node.parent:
        path.append(node.action)
        node = node.parent
    path.reverse()

    return path
