"""
    Enter your details below:

    Name: Jeff Yuanbo Han
    Student ID: u6617017
    Email: u6617017@anu.edu.au
"""

from search_strategies import SearchNode


def solve(problem):
    """ Return a list of directions. See handout for more details. """
    depth_limit = 0
    path = []  # The output path.
    while True:
        print('Optimal lower bound: {}'.format(depth_limit))

        # The closed list (of states already visited).
        # Note that it preserves the O(bm) space requirement.
        explored = []

        # Implement depth-limit search recursively.
        result = recursive_dls(SearchNode(problem.get_initial_state()),
                               problem, depth_limit, explored, path)
        if result == 'cutoff':
            depth_limit += 1
        elif result == 'success':
            path.reverse()
            return path
        else:  # result == 'failure', which means the goal is unreachable.
            print('Unreachable!')
            return None


def recursive_dls(node, problem, depth_limit, explored, path):
    explored.append(node.state)  # Add the state to explored.
    cut_off = False

    if problem.goal_test(node.state):
        return 'success'
    elif node.depth == depth_limit:
        cut_off = True
    else:
        for successor, action, cost in problem.get_successors(node.state):
            if successor in explored:
                continue

            result = recursive_dls(
                SearchNode(state=successor,
                           action=action,
                           path_cost=node.path_cost + cost,
                           depth=node.depth + 1),
                problem, depth_limit, explored, path)

            if result == 'cutoff':
                cut_off = True
            elif result == 'success':
                path.append(action)
                return 'success'

    # Remove this state from explored, to preserve the O(bm) memory requirement.
    explored.pop()

    if cut_off:
        return 'cutoff'
    else:
        return 'failure'
