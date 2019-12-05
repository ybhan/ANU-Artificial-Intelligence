from search_strategies import SearchNode
from frontiers import Stack


def dls_search(problem, depth_limit):
    # The frontier is a Stack (defined in frontiers.py), for its LIFO queuing policy.
    frontier = Stack()
    # Use SearchNode (defined in search_strategies.py) as the class of elements in frontier, and initialize frontier.
    frontier.push(SearchNode(problem.get_initial_state()))

    explored = []  # The closed list (of nodes already explored).

    while not frontier.is_empty():
        # Check the first node in frontier.
        node = frontier.pop()
        if problem.goal_test(node.state): return node
        if node.depth == depth_limit: continue

        for point in explored[::]:
            if point.depth > node.depth:
                explored.remove(point)

        # Expand this node if it is not the goal, nor does it reach the depth_limit.
        for successor, action, cost in problem.get_successors(node.state):
            # Avoid revisiting the explored states.
            if successor in [x.state for x in explored]:
                continue
            else:
                new_node = SearchNode(state=successor,
                                      action=action,
                                      path_cost=node.path_cost + cost,
                                      parent=node,
                                      depth=node.depth + 1
                                      )

                # Add the successor node to frontier and explored.
                frontier.push(new_node)
                explored.append(new_node)

    else:
        print(depth_limit)
        return 'cutoff'
