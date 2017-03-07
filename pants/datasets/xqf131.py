import os
import pandas as pd
from pants import Node, Position

def load_data():
    '''
    NAME : xqf131
    COMMENT : Bonn VLSI data set with 131 points
    COMMENT : Uni Bonn, Research Institute for Discrete Math
    COMMENT : Contributed by Andre Rohe
    TYPE : TSP
    DIMENSION : 131
    EDGE_WEIGHT_TYPE : EUC_2D
    NODE_COORD_SECTION


    '''
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xqf131.csv')
    dimensions = 131

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

'''
OPTIMAL PATH

http://www.math.uwaterloo.ca/tsp/vlsi/xqf131.tour.html

NAME: xqf131
COMMENT: Tour length 564
TYPE: TOUR
DIMENSION: 131
TOUR_SECTION
1
12
5
13
18
25
16
14
15
17
19
27
26
45
53
74
64
68
75
77
78
81
82
87
88
92
94
99
93
89
98
112
123
130
121
118
114
105
100
101
102
106
107
108
113
124
125
126
131
127
128
129
122
117
120
116
119
115
109
110
111
103
104
97
96
95
91
90
86
85
84
83
79
80
72
73
61
60
59
58
63
67
71
76
70
66
69
65
62
56
57
52
51
50
49
48
47
55
54
46
28
29
20
30
31
32
21
33
34
35
36
22
37
38
39
23
40
41
42
43
44
24
11
4
10
9
3
2
8
7
6
-1
EOF
'''