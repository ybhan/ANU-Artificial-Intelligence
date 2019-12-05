""" File name:   dfa.py
    Author:      Jeff Yuanbo Han (u6617017)
    Date:        6 March 2018
    Description: This file defines a function which reads in
                 a DFA described in a file and builds an appropriate datastructure.

                 There is also another function which takes this DFA and a word
                 and returns if the word is accepted by the DFA.

                 It should be implemented for Exercise 3 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""


def load_dfa(path_to_dfa_file):
    """ This function reads the DFA in the specified file and returns a
        data structure representing it. It is up to you to choose an appropriate
        data structure. The returned DFA will be used by your accepts_word
        function. Consider using a tuple to hold the parts of your DFA, one of which
        might be a dictionary containing the edges.

        We suggest that you return a tuple containing the names of the start
        and accepting states, and a dictionary which represents the edges in
        the DFA.

        (str) -> str, list, dict

        Output (tuple) structure: (initial, accepting, transition), where

        initial   : (str)  the initial state

        accepting : (list) list of strings of accepting states

        transition: (dict)
                    keys  : (str) current state
                    values: (dict)
                            keys  : (str) label on the outgoing edge
                            values: (str) successor state
    """
    # Define the output dictionary with 3 keys
    initial = ""
    accepting = []
    transition = {}

    with open(path_to_dfa_file) as dfa_file:
        for line in dfa_file:
            line = line.split()

            # Initial state (str)
            if line[0] == "initial":
                initial = line[1]
            # Accepting states (list)
            elif line[0] == "accepting":
                accepting.extend(line[1:])
            # Transitions (dict): structure as explained in the docstring
            elif line[1] in transition:
                transition[line[1]][line[3]] = line[2]
            else:  # Need definition for the first appearance
                transition[line[1]] = {line[3]: line[2]}

    return initial, accepting, transition


def accepts_word(dfa, word):
    """ This function takes in a DFA (that is produced by your load_dfa function)
        and then returns True if the DFA accepts the given word, and False
        otherwise.

        (tuple, str) -> bool
    """
    initial, accepting, transition = dfa

    state = initial  # Initialize the state
    for char in word:
        if char in transition[state]:
            state = transition[state][char]  # Update state
        else:  # No such outgoing edge -> Reject
            return False

    if state in accepting:  # An accepting state -> Accept
        return True
    else:  # Not an accepting state -> Reject
        return False
