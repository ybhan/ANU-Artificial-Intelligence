# minimax_agent.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

"""
    Enter your details below:

    Name: Jeff Yuanbo Han
    Student ID: u6617017
    Email: u6617017@anu.edu.au
"""

from agents import Agent
import util

from search_problems import AdversarialSearchProblem

class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
            (MinimaxAgent, str) -> None
        """
        self.max_player = max_player
        self.depth = int(depth)


    def evaluation(self, problem, state):
        """ The evaluation = (score
                              + catch_black / red_to_black
                              + yb_value * 0.5**red_dist
                              - yb_value * 0.5**black_dist)
            where:
            score = the current score;
            catch_black = 250, if the red bird has a chance to catch the black;
                        = 0, otherwise;
            red_to_black = the distance between the red and black bird;
            yb_value = the current value of a yellow bird;
            red_dist = the distance between the red bird and its 'reserved' food;
            black_dist = the distance between the black bird and its 'reserved' food.


            Here, we try to assign a 'reserved' food for each of the red and black bird.
            They are found as the most and least 'relatively close' yellow bird to the red bird,
            where 'relatively close' is quantified as
            the difference of distance to the red and to the black.

            The detailed procedure is:

            1. For all the yellow birds left, get the distance to the red bird.
               We then obtain a distance list: red_to_yellow.

            2. Likewise, get the distance to the black bird.
               We obtain another distance list: black_to_yellow.

            3. Now compute the difference: dist_diff = red_to_yellow .- black_to_yellow.
               Here, '.-' means minus item by item.

            4. Find the minimum in dist_diff, get the corresponding yellow bird.
               red_dist = the distance between this yellow bird to the red bird.

            5. Similarly, find the maximum in dist_diff, get the corresponding yellow bird.
               black_dist = the distance between this yellow bird to the black bird.


            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """
        player, red_pos, black_pos, yellow_birds, score, yb_value = state
        yellow_num = len(yellow_birds)

        red_to_black = problem.maze_distance(red_pos, black_pos)
        red_to_yellow = [problem.maze_distance(red_pos, prey) for prey in yellow_birds]
        black_to_yellow = [problem.maze_distance(black_pos, prey) for prey in yellow_birds]

        dist_diff = [(red_to_yellow[i]-black_to_yellow[i], i) for i in range(yellow_num)]
        dist_diff.sort()
        red_dist = red_to_yellow[dist_diff[0][1]]
        black_dist = black_to_yellow[dist_diff[-1][1]]

        # Compute the catch_black value.
        catch_black = 0
        # To catch the black, the first requirement is that:
        # the red bird has to move first when the red and black are next to each other.
        if red_to_black % 2 == 1 - player:
            # The second requirement is that:
            # the red bird has a possibility to be next to the black.
            if min(red_to_yellow) < max(black_to_yellow):
                catch_black = 250

        # Sum all the effects together.
        estimate = (score
                    + catch_black / red_to_black
                    + yb_value * 0.5**red_dist
                    - yb_value * 0.5**black_dist)

        return estimate


    def maximize(self, problem, state, current_depth, alpha=float('-inf'), beta=float('inf')):
        """ This method should return a pair (max_utility, max_action).
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.

             (MinimaxAgent, AdversarialSearchProblem,
                 (int, (int, int), (int, int), ((int, int)), number, number)
                     -> (number, str)
        """
        # Without alpha-beta pruning
        """
        max_action = 'Stop'
        if problem.terminal_test(state):
            max_utility = problem.utility(state)
        elif current_depth >= self.depth:
            max_utility = self.evaluation(problem, state)
        else:
            max_utility = float('-inf')
            for next_state, action, _ in problem.get_successors(state):
                utility = self.minimize(problem, next_state, current_depth+1)
                if utility > max_utility:
                    max_utility = utility
                    max_action = action

        return max_utility, max_action
        """
        # With alpha-beta pruning
        max_action = 'Stop'
        if problem.terminal_test(state):
            max_utility = problem.utility(state)
        elif current_depth >= self.depth:
            max_utility = self.evaluation(problem, state)
        else:
            max_utility = float('-inf')
            for next_state, action, _ in problem.get_successors(state):
                utility = self.minimize(problem, next_state, current_depth+1, alpha, beta)
                if utility > max_utility:
                    max_utility = utility
                    max_action = action
                if max_utility >= beta:
                    break
                alpha = max(alpha, max_utility)

        return max_utility, max_action


    def minimize(self, problem, state, current_depth, alpha=float('-inf'), beta=float('inf')):
        """ This function should just return the minimum utility.
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.

            (MinimaxAgent, AdversarialSearchProblem,
                 (int, (int, int), (int, int), ((int, int)), number, number)
                     -> number
        """
        # Without alpha-beta pruning
        """
        if problem.terminal_test(state):
            return problem.utility(state)
        elif current_depth >= self.depth:
            return self.evaluation(problem, state)
        else:
            min_utility = float('inf')
            for next_state, _, _ in problem.get_successors(state):
                min_utility = min(min_utility,
                                  self.maximize(problem, next_state, current_depth+1)[0])
            return min_utility
        """
        # With alpha-beta pruning
        if problem.terminal_test(state):
            return problem.utility(state)
        elif current_depth >= self.depth:
            return self.evaluation(problem, state)
        else:
            min_utility = float('inf')
            for next_state, _, _ in problem.get_successors(state):
                min_utility = min(min_utility,
                                  self.maximize(problem, next_state, current_depth+1, alpha, beta)[0])
                if min_utility <= alpha:
                    break
                beta = min(beta, min_utility)
            return min_utility


    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        # We tell the search problem what the current state is and which player
        # is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        print("At Root: Utility:", utility, "Action:", max_action, "Expanded:", problem._expanded)
        return max_action
