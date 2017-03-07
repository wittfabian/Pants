import time
import math
import argparse
import sys
from datetime import timedelta
import pandas as pd
import numpy as np

from pants import World, Edge, Node, Position
from pants import Solver

# Real-world latitude longitude coordinates.
TEST_COORDS_33_NEW = [
    Node(Position(34.021150, -84.267249)), Node(Position(34.021342, -84.363437)), Node(Position(34.022585, -84.362150)),
    Node(Position(34.022718, -84.361903)), Node(Position(34.023101, -84.362980)), Node(Position(34.024302, -84.163820)),
    Node(Position(34.044915, -84.255772)), Node(Position(34.045483, -84.221723)), Node(Position(34.046006, -84.225258)),
    Node(Position(34.048194, -84.262126)), Node(Position(34.048312, -84.208885)), Node(Position(34.048679, -84.224917)),
    Node(Position(34.049510, -84.226327)), Node(Position(34.051529, -84.218865)), Node(Position(34.055487, -84.217882)),
    Node(Position(34.056326, -84.200580)), Node(Position(34.059412, -84.216757)), Node(Position(34.060164, -84.242514)),
    Node(Position(34.060461, -84.237402)), Node(Position(34.061281, -84.334798)), Node(Position(34.063814, -84.225499)),
    Node(Position(34.061468, -84.334830)), Node(Position(34.061518, -84.243566)), Node(Position(34.062461, -84.240155)),
    Node(Position(34.064489, -84.225060)), Node(Position(34.066471, -84.217717)), Node(Position(34.068455, -84.283782)),
    Node(Position(34.068647, -84.283569)), Node(Position(34.071628, -84.265784)), Node(Position(34.105840, -84.216670)),
    Node(Position(34.109645, -84.177031)), Node(Position(34.116852, -84.163971)), Node(Position(34.118162, -84.163304))
]

# 45-45-90 triangle with unit length legs.
TEST_COORDS_3 = [
    (0, 0), (1, 0), (0, 1)
]

# Unit square with diagonals.
TEST_COORDS_4 = [
    (0, 0), (1, 0), (0, 1), (1, 1)
]

# Same as above except with additional node in center of left edge.
TEST_COORDS_5 = [
    (0, 0), (1, 0), (0, 1), (1, 1), (0, 0.5)
]

# TEST_COORDS_5_NEW = [
#     Node(Position(0, 0), name='A'),
#     Node(Position(1, 0), name='B'),
#     Node(Position(0, 1), name='C'),
#     Node(Position(1, 1), name='D'),
#     Node(Position(0, 0.5), name='E')
# ]

def dist(a, b):
    """Return the distance between two points represeted as a 2-tuple."""
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))


if __name__ == "__main__":
    world = World(TEST_COORDS_33_NEW, dist)
    solver = Solver(alpha=1, beta=5, rho=0.01, Q=1, t0=0.01, limit=100, ant_count=20, elite=0.5)

    # world.plot_nodes()
    solver_setting_report_format = "\n".join([
        "Solver settings:",
        "limit={w.limit}",
        "rho={w.rho}, Q={w.q}",
        "alpha={w.alpha}, beta={w.beta}",
        "elite={w.elite}"
    ])

    print(solver_setting_report_format.format(w=solver))

    columns = "{!s:<25}\t{:<25}"
    divider = "-" * (25 + 25)
    header = columns.format("Time Elapsed", "Distance")
    columns = columns.replace('<', '>', 1)

    print()
    print(header)
    print(divider)

    fastest = None
    fastest_time = None
    start_time = time.time()
    for i, ant in enumerate(solver.solutions(world)):
        fastest = ant
        fastest_time = timedelta(seconds=(time.time() - start_time))
        print(columns.format(fastest_time, ant.distance))
    total_time = timedelta(seconds=(time.time() - start_time))

    print(divider)
    print("Best solution:")
    for i, n in zip(fastest.visited, fastest.tour):
        print("  {:>8} = {}".format(i, n.position))

    print("Solution length: {}".format(fastest.distance))
    print("Found at {} out of {} seconds.".format(fastest_time, total_time))
    fastest.plot_tour()

    # world.print_pheromone_matrix()