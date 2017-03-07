import os
import pandas as pd
from pants import Node, Position

def load_data():
    '''
    NAME: usa115475
    TYPE: TSP
    COMMENT: 115,474 towns and cities in the United States
    COMMENT: Created July 7, 2012, www.math.uwaterloo/tsp/data/usa/
    DIMENSION: 115475
    EDGE_WEIGHT_TYPE: EUC_2D
    NODE_COORD_SECTION
    '''
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usa115475.csv')
    dimensions = 115475

    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    print('Load data ...')
    data = pd.read_csv(path, delimiter=' ', header=None)

    node_list = []
    for index, pos in data.iterrows():
        node_list.append(Node(Position(pos[0], pos[1])))

    if dimensions != len(node_list):
        raise Exception('Failed to load all examples. {} examples expected, got {}.'.format(dimensions, len(node_list)))

    print('Datapoints: {}'.format(dimensions))

    return node_list