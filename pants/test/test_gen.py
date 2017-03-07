import time
import math
import argparse
import sys
from datetime import timedelta
import pandas as pd
import numpy as np

from pants.datasets import xqf131, pma343

from pants import World, Edge, Node, Position
from pants import Solver

TEST_COORDS = pma343.load_data()

def dist(a, b):
    """Return the distance between two points represeted as a 2-tuple."""
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))


if __name__ == "__main__":
    world = World(TEST_COORDS, dist)
    solver = Solver(alpha=1, beta=5, rho=0.05, Q=1, t0=0.01, limit=100, ant_count=20, elite=0.5)

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