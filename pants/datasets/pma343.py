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
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pma343.csv')
    dimensions = 343

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

http://www.math.uwaterloo.ca/tsp/vlsi/pma343.tour

NAME: pma343
COMMENT: Tour length 1368
TYPE: TOUR
DIMENSION: 343
TOUR_SECTION
1
15
16
2
3
4
17
18
5
19
20
6
7
8
21
9
11
24
36
34
31
26
28
22
25
29
30
33
41
42
43
44
48
50
54
56
60
61
72
71
70
69
68
67
73
76
79
82
84
85
95
94
97
105
104
103
101
100
102
109
118
119
120
121
122
123
124
126
129
131
133
134
135
143
142
146
145
144
149
152
150
153
151
155
161
160
159
157
148
154
158
171
172
163
164
165
166
167
173
174
175
183
190
189
188
187
185
181
182
176
177
178
180
186
196
197
198
199
200
201
202
209
205
208
211
214
221
226
229
239
240
241
242
243
244
250
249
255
257
253
248
247
238
237
246
236
235
234
245
252
254
256
261
260
262
270
278
279
277
276
271
263
264
265
272
266
267
268
273
274
275
280
281
282
292
291
290
289
298
297
296
301
307
302
308
303
312
319
325
341
336
340
343
342
339
338
335
334
332
330
331
333
337
329
321
322
323
326
327
328
324
318
317
316
315
314
311
306
310
305
300
304
309
320
313
299
285
286
287
293
294
295
288
284
283
269
259
258
251
231
232
233
230
223
227
228
225
224
222
220
219
218
217
216
215
212
206
213
210
207
204
195
194
193
192
203
191
184
179
170
169
168
162
156
147
138
139
140
141
137
127
132
136
130
128
125
117
116
115
114
113
112
110
111
108
107
106
98
99
96
86
87
88
89
90
91
92
93
81
78
75
77
83
80
74
63
64
65
66
62
51
49
53
55
57
58
59
52
47
46
40
39
38
37
45
35
32
27
23
10
12
13
14
-1
EOF
'''