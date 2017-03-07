=====
Pants
=====

A Python3 implementation of the Ant Colony Optimization Meta-Heuristic

**Installation is not possible at this time. Repository is under development.**

--------
Overview
--------

**Pants** provides you with the ability to quickly determine how to
visit a collection of interconnected nodes such that the work done is
minimized. Nodes can be any arbitrary collection of data while the edges
represent the amount of "work" required to travel between two nodes.
Thus, **Pants** is a tool for solving traveling salesman problems.

The world is built from a list of nodes and a function responsible for
returning the length of the edge between any two given nodes. The length
function need not return actual length. Instead, "length" refers to that 
the amount of "work" involved in moving from the first node to the second
node - whatever that "work" may be. For a silly, random example, it could
even be the number of dishes one must wash before moving to the next 
station at a least dish-washing dish washer competition.

Solutions are found through an iterative process. In each iteration,
several ants are allowed to find a solution that "visits" every node of
the world. The amount of pheromone on each edge is updated according to
the length of the solutions in which it was used. The ant that traveled the
least distance is considered to be the local best solution. If the local
solution has a shorter distance than the best from any previous
iteration, it then becomes the global best solution. The elite ant(s)
then deposit their pheromone along the path of the global best solution
to strengthen it further, and the process repeats.

You can read more about `Ant Colony Optimization on
Wikipedia <http://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms>`_.

------------
Installation
------------

Installation via ``pip``

.. code-block:: console

    $ pip3 install ACO-Pants

-----
Usage
-----

Using **Pants** is simple. The example here uses Euclidean distance
between 2D nodes with ``(x, y)`` coordinates, but there are no real
requirements for node data of any sort.

1) Import **Pants** (along with any other packages you'll need).

   .. code-block:: python

        import pants
        import math
        import random

2) Create your data points; these become the nodes. Here we create some
   random 2D points. The only requirement for a node is that it is
   distinguishable from all of the other nodes.

   .. code-block:: python

      nodes = []
      for _ in range(20):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        nodes.append(Node(Position(x, y)))


3) Define your length function. This function must accept two nodes and
   return the amount of "work" between them. In this case, Euclidean 
   distance works well.

   .. code-block:: python

      def euclidean(a, b):
          return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

4) Create the ``World`` from the nodes and the length function. 

   .. code-block:: python

        world = pants.World(nodes, euclidean)

5) Create the ``Solver``.

   .. code-block:: python

        solver = pants.Solver()

6) Solve the ``World`` with the ``Solver``. Two methods are provided for
   finding solutions: ``solve()`` and ``solutions()``. The former
   returns the best solution found, whereas the latter returns each
   solution found if it is the best thus far.

   .. code-block:: python

        solution = solver.solve(world)
        # or
        solutions = solver.solutions(world)

7) Inspect the solution(s).

   .. code-block:: python

        print(solution.distance)
        print(solution.tour)    # Nodes visited in order
        print(solution.path)    # Edges taken in order
        # or
        best = float("inf")
        for solution in solutions:
          assert solution.distance < best
          best = solution.distance


Known Bugs
----------

None of which I am currently aware. Please let me know if you find 
otherwise.

Troubleshooting
---------------

Credits
-------

-  Robert Grant rhgrant10@gmail.com

License
-------

GPL
