import time
import math
import argparse
import sys
from datetime import timedelta
import pandas as pd

from pants import World, Edge
from pants import Solver

# Real-world latitude longitude coordinates.
TEST_COORDS_33 = [
    (34.021150, -84.267249), (34.021342, -84.363437), (34.022585, -84.362150),
    (34.022718, -84.361903), (34.023101, -84.362980), (34.024302, -84.163820),
    (34.044915, -84.255772), (34.045483, -84.221723), (34.046006, -84.225258),
    (34.048194, -84.262126), (34.048312, -84.208885), (34.048679, -84.224917),
    (34.049510, -84.226327), (34.051529, -84.218865), (34.055487, -84.217882),
    (34.056326, -84.200580), (34.059412, -84.216757), (34.060164, -84.242514),
    (34.060461, -84.237402), (34.061281, -84.334798), (34.063814, -84.225499),
    (34.061468, -84.334830), (34.061518, -84.243566), (34.062461, -84.240155),
    (34.064489, -84.225060), (34.066471, -84.217717), (34.068455, -84.283782),
    (34.068647, -84.283569), (34.071628, -84.265784), (34.105840, -84.216670),
    (34.109645, -84.177031), (34.116852, -84.163971), (34.118162, -84.163304)
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

def dist(a, b):
    """Return the distance between two points represeted as a 2-tuple."""
    return math.sqrt((a[1] - b[1]) ** 2 + (a[0] - b[0]) ** 2)


if __name__ == "__main__":
    world = World(TEST_COORDS_33, dist)
    solver = Solver(alpha=1, beta=3, rho=0.8, Q=1, t0=0.01, limit=100, ant_count=10, elite=0.5)

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
    start_time = time.time()
    for i, ant in enumerate(solver.solutions(world)):
        fastest = ant
        fastest_time = timedelta(seconds=(time.time() - start_time))
        print(columns.format(fastest_time, ant.distance))
    total_time = timedelta(seconds=(time.time() - start_time))

    print(divider)
    print("Best solution:")
    for i, n in zip(fastest.visited, fastest.tour):
        print("  {:>8} = {}".format(i, n))

    print("Solution length: {}".format(fastest.distance))
    print("Found at {} out of {} seconds.".format(fastest_time, total_time))

    # world.print_pheromone_matrix()