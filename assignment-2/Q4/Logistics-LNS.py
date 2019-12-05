""" File name:   Logistics-LNS.py
    Author:      Jeff Yuanbo Han
    Date:        2018-05-04
    Description: This file should implement a Large Neighborhood Search (LNS)
                 for the Logistics Problem for Q4 of Assignment 2.
                 See the assignment notes for a description of its contents.
"""
import argparse
import subprocess
import random


def LNS(problem, solution, k=10, iteration=10):
    for search_iter in range(iteration):
        # Read the start solution
        with open(solution, 'r') as solu:
            s_lines = solu.readlines()

        for row in range(len(s_lines)):
            print(s_lines[row].rstrip())

        tot_cost = s_lines[0].split()[-1]

        # Randomly destroy k phases of the solution
        destroy = random.choices(range(1,len(s_lines)), k=k)

        # Some operations on the strings
        s = []
        for i in range(1,len(s_lines)):
            if i not in destroy:
                s_lines[i] = s_lines[i].strip()
                s.append(s_lines[i].split(','))

        # Extract neighborhood constraints
        s_str = []
        for i in range(len(s)):
            s_str.append("constraint trans[{},{},1] = {};\n".format(s[i][0], s[i][2], s[i][3]))
            s_str.append("constraint trans[{},{},2] = {};\n".format(s[i][0], s[i][2], s[i][4]))
            s_str.append("constraint step[{},{}] = {};\n".format(s[i][0], s[i][2], s[i][1]))

        # Write in keep.dzn the constraints as well as the parameters
        with open("keep.dzn", 'w') as l:
            with open(problem) as p:
                l.writelines(p.readlines())
            l.write("\n% Constraints from the previous solution\n")
            l.writelines(s_str)

        # Boost MiniZinc to search for a local optima (Repair)
        command = "minizinc Logistics-opt.mzn --soln-sep '' --search-complete-msg '' > best{}"\
            .format(solution.lstrip("starbe"))

        result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
        output = result.stdout
        print(output.decode("utf-8"))

        solution = "best{}".format(solution.lstrip("starbe"))


# Make it work in command lines
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('problem_filename', help='problem file')
    parser.add_argument('start_solution_filename', help='file describing the solution to improve')
    parser.add_argument('k', help='number of phases to destroy each iteration')
    parser.add_argument('iter', help='number of total iterations')
    args = parser.parse_args()
    start_solution_filename = args.start_solution_filename
    problem_filename = args.problem_filename
    k = int(args.k)
    iteration = int(args.iter)

    LNS(problem_filename, start_solution_filename, k, iteration)
