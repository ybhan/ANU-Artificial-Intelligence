""" File name:   math_functions.py
    Author:      Jeff Yuanbo Han (u6617017)
    Date:        4 March 2018
    Description: This file defines a set of variables and simple functions.

                 It should be implemented for Exercise 1 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""

import math

ln_e = math.log(math.e)

twenty_radians = math.radians(20)


def quotient_ceil(numerator, denominator):
    """ Return the ceiling of the result of the division (numerator divided by the denominator).

        (number, number) -> int
    """
    return math.ceil(numerator / denominator)


def quotient_floor(numerator, denominator):
    """ Return the floor of the result of the division (numerator divided by the denominator).

        (number, number) -> int
    """
    return math.floor(numerator / denominator)


def manhattan(x1, y1, x2, y2):
    """ Return the Manhattan distance between (x1, y1) and (x2, y2).

        (number, number, number, number) -> number
    """
    return abs(x1 - x2) + abs(y1 - y2)
