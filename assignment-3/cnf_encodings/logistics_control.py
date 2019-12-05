# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" Student Details

    Student Name: Jeff Yuanbo Han
    Student ID: u6617017
    Email: u6617017@anu.edu.au
    Date: 2018-05-25
"""

"""
    In this file you will implement some constraints which represent
    domain-specific control knowledge for the Logistics domain
    (benchmarks/logistics).

    These constraints will be used in addition to a standard flat encoding of
    the Logistics problem instances, without plan graph mutexes (which you are
    assumed to have completed while going through Exercises 1-6).

    Those constraints should make solving the problem easier. This may be at
    the cost of optimality. That is, your additional constraints may rule out
    some solutions to make planning easier -- for example, by restricting the
    way trucks and planes can move -- but they should preserve SOME solution
    (the problems might be very easy to solve if you added a contradiction, but
    wholly uninteresting!).

    Often control knowledge for planning problems is based on LTL (Linear
    Temporal Logic - https://en.wikipedia.org/wiki/Linear_temporal_logic) and
    you might get inspired by studying this.

    We do not expect you to implement an automatic compilation of arbitrary LTL
    into SAT, just some control knowledge rules for problems from the Logistics
    domain.

    As an example rule to get you started, you could assert that if a package
    was at its destination, then it cannot leave.

    That is you could iterate over the goal of the problem to find the
    propositions which talk about where the packages should end up and make
    some constraints asserting that if one of the corresponding fluents is true
    at step t then it must still be true at step t + 1

    You will be marked based on the correctness, inventiveness, and
    effectiveness of the control knowledge you devise.

    You should aim to make at least three different control rules. Feel free to
    leave (but comment out) rules which you abandon if you think they are
    interesting and want us to look at them.

    Use the flag "-e logistics" to select this encoding and the flag "-p false"
    to disable the plangraph mutexes.
"""

from strips_problem import Action, Proposition

from .basic import BasicEncoding

from itertools import product, combinations

encoding_class = 'LogisticsEncoding'


class LogisticsEncoding(BasicEncoding):
    """ An encoding which extends BasicEncoding but adds control knowledge
        specific for the Logistics domain.
    """

################################################################################
#                You need to implement the following methods                   #
################################################################################

    def make_control_knowledge_variables(self, horizon):
        """ Make the variable for the problem.

            Use the function self.new_cnf_code(step, name, object) to make
            whatever codes for CNF variables you need to make your control
            knowledge for the Logistics problem.

            You can make variables which mean anything if you can think of
            constraints to make that enforce that meaning. As an example, if
            you were making control logic for the miconics domain, you might
            make variables which keep track if each passenger has ever
            been in an elevator and is now not.

            For a passenger p, and t > 0:
                was_boarded(p)@t <->
                    (-boarded(p)@t ^ (boarded(p)@t-1 v was_boarded(p)@t-1))

            You can then use these variables, along with the fluent and action
            variables to make your control knowledge.

            (LogisticsEncoding, int) -> None
        """
        # You might want to save your variables here, or feel free to make as many data
        # structures as you need to keep track of them.
        self.control_fluent_codes = {}

        """ *** YOUR CODE HERE *** """
        # Predicate (plane-visited-airport ?plane ?airport): plane has ever landed at airport
        fly_planes = {a for a in self.problem.actions if a.name == 'fly-airplane'}
        self.problem.planes = {fly_plane.parameters[0] for fly_plane in fly_planes}
        self.problem.airports = {fly_plane.parameters[1] for fly_plane in fly_planes}

        self.plane_visited_airports = []  # to store all the (plane-visited-airport plane airport)@t fluents
        for plane, airport in product(self.problem.planes, self.problem.airports):
            plane_visited_airport = Proposition('plane-visited-airport', [plane, airport])
            self.plane_visited_airports.append(plane_visited_airport)
            for t in range(horizon+1):
                self.control_fluent_codes[(plane_visited_airport, t)] = \
                    self.new_cnf_code(t, str(plane_visited_airport), plane_visited_airport)

        # Predicate (same-city ?loc1 ?loc2): loc1 and loc2 are in the same city
        self.problem.locations = {p.variables[0] for p in self.problem.propositions if p.name == 'in-city'}
        self.problem.cities = {p.variables[1] for p in self.problem.propositions if p.name == 'in-city'}

        self.same_cities = []  # to store all the (same-city loc1 loc2)@0 fluents
        for loc1, loc2 in combinations(self.problem.locations, 2):
            same_city = Proposition('same-city', [loc1, loc2])
            self.same_cities.append(same_city)
            # Only step 0 is enough
            self.control_fluent_codes[(same_city, 0)] = self.new_cnf_code(0, str(same_city), same_city)

    def make_control_knowledge(self, horizon):
        """ This is where you should make your control knowledge clauses.

            These clauses should have the type "control".

            (LogisticsEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """
        # 1. Packages remain at their goal position once they reach there
        for p in self.problem.propositions:
            if p in self.problem.goal:
                for t in range(horizon):
                    self.add_clause([-self.proposition_fluent_codes[(p, t)],
                                     self.proposition_fluent_codes[(p, t+1)]], 'control')

        # 2. A plane cannot land twice at the same airport
        for plane_visited_airport in self.plane_visited_airports:
            # -(plane-visited-airport plane airport)@0 (i.e. initial location is not regarded as 'visited')
            self.add_clause([-self.control_fluent_codes[(plane_visited_airport, 0)]], 'control')

            # (plane-visited-airport plane airport)@t+1 <->
            # (plane-visited-airport plane airport)@t \/ (at plane airport)@t+1
            for p in self.problem.propositions:
                if p.name == 'at' and p.variables == plane_visited_airport.variables:
                    for t in range(horizon):
                        self.add_clause([-self.control_fluent_codes[(plane_visited_airport, t+1)],
                                         self.control_fluent_codes[(plane_visited_airport, t)],
                                         self.proposition_fluent_codes[(p, t+1)]], 'control')
                        self.add_clause([-self.control_fluent_codes[(plane_visited_airport, t)],
                                         self.control_fluent_codes[(plane_visited_airport, t+1)]], 'control')
                        self.add_clause([self.control_fluent_codes[(plane_visited_airport, t+1)],
                                         -self.proposition_fluent_codes[(p, t+1)]], 'control')

            # (plane-visited-airport plane airport)@t -> -(fly-airplane plane any_airport airport)@t+1
            for a in self.problem.actions:
                if a.name == 'fly-airplane' and a.parameters[0::2] == plane_visited_airport.variables:
                    for t in range(horizon-1):
                        self.add_clause([-self.control_fluent_codes[(plane_visited_airport, t)],
                                         -self.action_fluent_codes[(a, t+1)]], 'control')

        # 3. load-truck only if the package is at initial location or at the same city with its goal
        # (same-city loc1 loc2)@0 <-> loc1.name and loc2.name have the same prefix (for example 'city2-1', 'city2-4')
        for same_city in self.same_cities:
            loc1, loc2 = same_city.variables
            if loc1.split('-')[0] == loc2.split('-')[0]:
                self.add_clause([self.control_fluent_codes[(same_city, 0)]], 'control')
            else:
                self.add_clause([-self.control_fluent_codes[(same_city, 0)]], 'control')

        # (load-truck package truck loc)@t -> (at package loc)@0 \/ (same-city loc package's_goal_loc)@0
        for a, p, goal, same_city in \
                product(self.problem.actions, self.problem.propositions, self.problem.goal, self.same_cities):
            if a.name == 'load-truck' and p.name == 'at' and a.parameters[0::2] == p.variables \
                    and goal.variables[0] == a.parameters[0] \
                    and same_city.variables == [a.parameters[2], goal.variables[1]]:
                for t in range(horizon):
                    self.add_clause([-self.action_fluent_codes[(a, t)],
                                     self.proposition_fluent_codes[(p, 0)],
                                     self.control_fluent_codes[(same_city, 0)]], 'control')

################################################################################
#                    Do not change the following method                        #
################################################################################

    def encode(self, horizon, exec_semantics, plangraph_constraints):
        """ Make an encoding of self.problem for the given horizon.

            For this encoding, we have broken this method up into a number
            of sub-methods that you need to implement.

           (LogisticsEncoding, int, str, str) -> None
        """
        super().encode(horizon, exec_semantics, plangraph_constraints)
        self.make_control_knowledge_variables(horizon)
        self.make_control_knowledge(horizon)
