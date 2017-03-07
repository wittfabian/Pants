import time
import math
import argparse
import sys
from datetime import timedelta
import pandas as pd
import numpy as np
import operator

from pants import Solver,World, Edge, Node, Position, SelectionMechanism

TEST_WEIGHTS_5 = [
    1.0, 2.0, 3.0, 4.0, 5.0
]



if __name__ == "__main__":
    selection = SelectionMechanism(TEST_WEIGHTS_5)
    print(selection._probabilities)

    # print(selection.roulette_wheel_selection())

    # print(selection.tournament_selection(q=None, relate=operator.gt))
