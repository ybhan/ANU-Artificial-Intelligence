""" File name:   truth_tables.py
    Author:      Jeff Yuanbo Han (u6617017)
    Date:        4 March 2018
    Description: This file defines a number of functions which implement Boolean
                 expressions.

                 It also defines a function to generate and print truth tables
                 using these functions.

                 It should be implemented for Exercise 2 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""


def boolean_fn1(a, b, c):
    """ Return the truth value of (a ∨ b) → (-a ∧ -b) """
    return not (a or b) or not a and not b


def boolean_fn2(a, b, c):
    """ Return the truth value of (a ∧ b) ∨ (-a ∧ -b) """
    return a and b or not a and not b


def boolean_fn3(a, b, c):
    """ Return the truth value of ((c → a) ∧ (a ∧ -b)) ∨ (-a ∧ b) """
    return (not c or a) and a and not b or not a and b


def draw_truth_table(boolean_fn):
    """ This function prints a truth table for the given boolean function.
        It is assumed that the supplied function has three arguments.

        ((bool, bool, bool) -> bool) -> None

        If your function is working correctly, your console output should look
        like this:

        >>> from truth_tables import *
        >>> draw_truth_table(boolean_fn1)
        a     b     c     res
        -----------------------
        True  True  True  False
        True  True  False False
        True  False True  False
        True  False False False
        False True  True  False
        False True  False False
        False False True  True
        False False False True
    """

    # Regularize the print format of each line
    print_format = "%-6s" * 3 + "%s"

    # Line 1 and 2
    print(print_format % ("a", "b", "c", "res"))
    print("-" * 23)
    # Line 3 to 10
    for a in (1, 0):
        for b in (1, 0):
            for c in (1, 0):
                tup = (a, b, c, boolean_fn(a, b, c))
                print(print_format % tuple(map(bool, tup)))

    return None
