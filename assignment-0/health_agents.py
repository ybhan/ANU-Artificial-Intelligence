""" File name:   health_agents.py
    Author:      Jeff Yuanbo Han (u6617017)
    Date:        8 March 2018
    Description: This file contains agents which fight disease. It is used
                 in Exercise 4 of Assignment 0.
"""

import random


class HealthAgent:
    """ A simple disease fighting agent. """

    def __init__(self, locations, conn):
        """ This constructor does nothing except save the locations and conn.
            Feel free to overwrite it when you extend this class if you want
            to do some initial computation.

            (HealthAgent, [str], { str : set([str]) }) -> None
        """
        self.locations = locations
        self.conn = conn

    def choose_move(self, location, valid_moves, disease, threshold, growth, spread):
        """ Using given information, return a valid move from valid_moves.
            Returning an invalid move will cause the system to stop.

            Changing any of the mutable parameters will have no effect on the operation
            of the system.

            This agent will locally move to the highest disease, of there is
            is no nearby disease, it will act randomly.

            (HealthAgent, str, [str], [str], { str : float }, float, float, float) -> str
        """
        max_disease = None
        max_move = None
        for move in valid_moves:
           if max_disease is None or disease[move] > max_disease:
               max_disease = disease[move]
               max_move = move

        if not max_disease:
            return random.choice(valid_moves)

        return max_move


# Make a new agent here called SmartHealthAgent, which extends HealthAgent and
# acts a bit more sensibly. Feel free to add other helper functions if needed.

class SmartHealthAgent(HealthAgent):
    """ A smart disease fighting agent. This agent will move one step along a shortest path
        to somewhere. That path has the highest priority of all shortest path to reachable locations.

        It is accomplished in 3 steps:
        1. For each reachable places, find by Uniform Cost Search a shortest path from location to it.
        2. Compute the severity of each node, and then compute the priority of each path obtained in 1.
        3. Move one step along a path with the highest priority.

        See more details for step-1 in uc_search method, and for step-2 and 3 in choose_move method.
    """
    def __init__(self, locations, conn):
        """ Save the locations and conn as HealthAgent do.

            (HealthAgent, [str], { str : set([str]) }) -> None
        """
        super().__init__(locations, conn)

    def choose_move(self, location, valid_moves, disease, threshold, growth, spread):
        """ First, derive the distance as well as a shortest path from location to each reachable node,
            by the method of Uniform Cost Search Algorithm. Then compute related statistics (defined
            below). Finally, move one step along a path with the highest priority.

            Define a statistic for each node called "severity":

            severity[loc] = disease[loc] * len(conn[loc]), if disease[loc] < threshold;
                            disease[loc] ** 2 / threshold * len(conn[loc]), otherwise.

            severity(loc) depicts very well how serious the pandemic is in loc.
            Two essential features are reflected:
            1. It is much more serious when disease[loc] >= threshold, because it spreads to its neighbors.
            2. The potential threat to neighbors is counted in by multiplying len(conn[loc]).
               For example, a location with 3 neighbors is intuitively more serious than another of the
               same disease level but with 2 neighbors.

            Define the "priority" of a road (a path from location to somewhere) as:

            priority[road] = sum([severity[loc] for node in road]) / dist(road_target),
                             where road_target is the final destination of this road.

            This to some extent reflects the average severity of nodes in a path.

            Based on discussions above, all that we need now is moving one step along a path with the
            highest priority.

            (SmartHealthAgent, str, [str], [str], {str: float}, float, float, float) -> str
        """
        from operator import itemgetter

        move = None

        # Find the distance as well as a shortest path from location to each reachable node.
        dist, path = self.uc_search(location)

        # Compute severity for each nodes.
        severity = {}
        for loc in self.locations:
            if disease[loc] < threshold:
                severity[loc] = disease[loc] * len(self.conn[loc])
            else:
                severity[loc] = disease[loc] ** 2 / threshold * len(self.conn[loc])

        # Compute priority for each shortest path.
        priority = {location: severity[location]}
        for target in path:
            priority[target] = sum([severity[node] for node in path[target]]) / dist[target]

        # Move one step along a path with the highest priority.
        ranking = sorted(priority.items(), key=itemgetter(1), reverse=True)
        ranked_targets = [x[0] for x in ranking]
        for target in ranked_targets:
            if target == location:
                move = location
                break
            else:
                move = path[target][1]
                break

        # If there is no reachable node at all, just hopelessly move in random.
        if not move:
            return random.choice(valid_moves)

        return move

    def uc_search(self, location):
        """ Call: dist, path = self.uc_search(location)

            Compute the distances from location to any other place in self.locations
            by Uniform Cost Search. (We shall call each of the locations a node.)
            The distance to an unreachable node is set as inf (i.e. math.inf).

            The output is
            dist: { "X" : the shortest distance from location to X }
            path: { "X" : [a shortest path from location to X] }
                  where X goes through all nodes in self.locations.
                  However in path, X must be reachable (i.e. dist[X] < inf).

            (SmartHealthAgent, str) -> {str: num}, {str: [str]}
        """
        from math import inf

        # Restore [self.locations] in a set {locations}, in case that the returned paths
        # are determined by the order in [self.locations].
        locations = set(self.locations)

        dist = dict((loc, inf) for loc in locations)  # Initialize all distances as inf.
        dist[location] = 0  # The distance is 0 from location to itself.
        path = {}

        current = location  # The currently being-operated node, starting with location.
        visited = set()  # The set of nodes that have already been visited.

        while len(visited) < len(locations):
            visited.add(current)
            # Check new connected nodes, and update the distance if it shortens.
            for neighbor in self.conn[current]:
                if dist[current] + 1 < dist[neighbor]:
                    dist[neighbor] = dist[current] + 1
                    path[neighbor] = [current]  # Record the last node passed by.

            # Choose a nearest unvisited node to operate for the next loop.
            # This selection will be arbitrary if there exists more than one candidate,
            # since {locations} is a set with no order.
            candidate_dist = inf
            for candidate in locations:
                if candidate in visited: continue
                if dist[candidate] < candidate_dist:
                    candidate_dist = dist[candidate]
                    current = candidate
            # No candidates? Because all remaining nodes are isolated! Must break.
            if current in visited: break

        # Connect all the passing-by nodes to obtain complete paths.
        for target in path:
            while path[target][-1] != location :
                path[target].extend( path[ path[target][-1] ] )

        # Invert the order and add the final destination to each path.
        for target in path:
            path[target].reverse()
            path[target].append(target)

        return dist, path
