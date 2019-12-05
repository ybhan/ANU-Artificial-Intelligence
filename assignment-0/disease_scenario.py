""" File name:   disease_scenario.py
    Author:      Jeff Yuanbo Han (u6617017)
    Date:        7 March 2018
    Description: This file represents a scenario simulating the spread of an
                 infectious disease around Australia. It should be
                 implemented for Part 1 of Exercise 4 of Assignment 0.

                 See the lab notes for a description of its contents.
"""


class DiseaseScenario:
    def __init__(self):
        """ Create the following variables with the (empty) specified types:

            threshold — float
            growth    — float
            spread    — float
            location  — str
            locations — list
            disease   — dict
            conn      — dict

            (DiseaseScenario) -> None
        """
        self.threshold = float()
        self.growth = float()
        self.spread = float()
        self.location = ""
        self.locations = []
        self.disease = {}
        self.conn = {}

    def read_scenario_file(self, path_to_scenario_file):
        """ Read a scenario from the given file and store the relevant information.
            Return True if successful, and False in the case an IOError occurs.

            (DiseaseScenario, str) -> bool
        """
        try:
            with open(path_to_scenario_file) as scenario_file:
                for line in scenario_file:
                    line = line.split()
                    if line[0] == "threshold": self.threshold = float(line[1])
                    elif line[0] == "growth": self.growth = float(line[1])
                    elif line[0] == "spread": self.spread = float(line[1])
                    elif line[0] == "start": self.location = line[1]
                    elif line[0] == "location": self.locations.append(line[1])
                    elif line[0] == "disease": self.disease[line[1]] = float(line[2])
                    elif line[0] == "conn":
                        # Roads are symmetrical. Need definition for first time.
                        if line[1] in self.conn: self.conn[line[1]].add(line[2])
                        else: self.conn[line[1]] = {line[2]}
                        if line[2] in self.conn: self.conn[line[2]].add(line[1])
                        else: self.conn[line[2]] = {line[1]}

            # Other locations have 0 disease by default.
            for loc in self.locations:
                if loc not in self.disease:
                    self.disease[loc] = 0

        # Detect IOError
        except IOError: return False
        else: return True

    def valid_moves(self):
        """ Return a list of valid moves. Each valid move is either a neighbouring
            location or the current location of the agent.

            (DiseaseScenario) -> [str]
        """
        return [self.location] + list(self.conn[self.location])

    def move(self, loc):
        """ Move the agent to the specified location and clear the disease there.
            If the method attempts to move the agent to a location that is invalid
            given the current location, a ValueError will be raised. The agent is
            allowed to stay where it is.

            (DiseaseScenario, str) -> None
        """
        if loc in self.valid_moves():
            self.location = loc
            self.disease[loc] = 0
        else: raise ValueError

    def spread_disease(self):
        """ Perform growth and spreading of the disease.

            Rules are:
            1. Disease grows and spreads at all locations at the same time.
            2. Disease only spreads to adjacent locations if the spreading location
               has greater than or equal to the threshold level of disease.
            3. Disease will not grow at or spread to the location where the agent is.

            (DiseaseScenario) -> None
        """
        # Store the current state of disease for convenience of simultaneity.
        disease = dict(self.disease)

        # Update self.disease at all locations.
        for loc in self.locations:
            # Growth
            self.disease[loc] += disease[loc] * self.growth
            # Spreading
            if disease[loc] >= self.threshold:
                for neighbor in self.conn[loc]:
                    self.disease[neighbor] += disease[loc] * self.spread

        # Fix a detail: disease will not grow at or spread to the location of the agent.
        self.disease[self.location] = disease[self.location]
