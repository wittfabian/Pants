"""
.. module:: world
    :platform: Linux, Unix, Windows
    :synopsis: Provides classes for representing a world and its edges.

.. moduleauthor:: Robert Grant <rhgrant10@gmail.com>

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class World:
    """The nodes and edges of a particular problem.

    Each :class:`World` is created from a list of nodes, a length function, and
    optionally, a name and a description. Additionally, each :class:`World` has
    a UID. The length function must accept nodes as its first two parameters,
    and is responsible for returning the distance between them. It is the 
    responsibility of the :func:`create_edges` to generate the required
    :class:`Edge`\s and initialize them with the correct *length* as returned
    by the length function.
    
    Once created, :class:`World` objects convert the actual nodes into node
    IDs, since solving does not rely on the actual data in the nodes. These are
    accessible via the :attr:`nodes` property. To access the actual nodes,
    simply pass an ID obtained from :attr:`nodes` to the :func:`data` method,
    which will return the node associated with the specified ID.
    
    :class:`Edge`\s are accessible in much the same way, except two node IDs
    must be passed to the :func:`data` method to indicate which nodes start and
    end the :class:`Edge`. For example:
    
    .. code-block:: python
    
        ids = world.nodes
        assert len(ids) > 1
        node0 = world.data(ids[0])
        node1 = world.data(ids[1])
        edge01 = world.data(ids[0], ids[1])
        assert edge01.start == node0
        assert edge01.end == node1
    
    The :func:`reset_pheromone` method provides an easy way to reset the
    pheromone levels of every :class:`Edge` contained in a :class:`World` to a
    given *level*. It should be invoked before attempting to solve a 
    :class:`World` unless a "blank slate" is not desired. Also note that it
    should *not* be called between iterations of the :class:`Solver` because it
    effectively erases the memory of the :class:`Ant` colony solving it.
        
    :param list nodes: a list of nodes
    :param callable lfunc: a function that calculates the distance between
                           two nodes
    :param str name: the name of the world (default is "world#", where
                     "#" is the ``uid`` of the world)
    :param str description: a description of the world (default is None)
    """
    uid = 0

    def __init__(self, nodes, lfunc, **kwargs):
        self.uid = self.__class__.uid
        self.__class__.uid += 1
        self.name = kwargs.get('name', 'world{}'.format(self.uid))
        self.description = kwargs.get('description', None)
        if all(isinstance(n, Node) for n in nodes):
            self._nodes = nodes
        elif all(isinstance(n, Position) for n in nodes):
            self._nodes = []
            for pos in nodes:
                self._nodes.append(Node(pos))
        else:
            raise Exception('Type of nodes not known!')
        self.lfunc = lfunc
        self.edges = self.create_edges()
        
    @property
    def nodes(self):
        """Node IDs."""
        # return list(range(len(self._nodes)))
        node_list = []
        for node in self._nodes:
            node_list.append(node.uid)
        return node_list

    def create_edges(self):
        """Create edges from the nodes.
        
        The job of this method is to map node ID pairs to :class:`Edge`
        instances that describe the edge between the nodes at the given
        indices. Note that all of the :class:`Edge`\s are created within this
        method.
        
        :return: a mapping of node ID pairs to :class:`Edge` instances.
        :rtype: :class:`ndarray`
        """
        # edges = {}
        edges = np.ndarray((len(self._nodes), len(self._nodes)), dtype=np.object)
        for m in self._nodes:
            for n in self._nodes:
                if m != n:
                    edge = Edge(m, n, lfunc=self.lfunc)
                    edges[m.uid, n.uid] = edge

        return edges

    def list_edges(self):
        edges = []
        for m in self._nodes:
            for n in self._nodes:
                if m != n:
                    edges.append(self.edges[m.uid, n.uid])
        return edges
        
    def reset_pheromone(self, level=0.01):
        """Reset the amount of pheromone on every edge to some base *level*.
        
        Each time a new set of solutions is to be found, the amount of
        pheromone on every edge should be equalized to ensure un-biased initial
        conditions. 
        
        :param float level: amount of pheromone to set on each edge 
                            (default=0.01)
        """
        for index, edge in np.ndenumerate(self.edges):
            if isinstance(edge, Edge):
                edge.pheromone = level

    def data(self, idx, idy=None):
        """Return the node data of a single id or the edge data of two ids.

        If only *idx* is specified, return the node with the ID *idx*. If *idy*
        is also specified, return the :class:`Edge` between nodes with indices
        *idx* and *idy*.

        :param int idx: the id of the first node
        :param int idy: the id of the second node (default is None)
        :return: the node with ID *idx* or the :class:`Edge` between nodes
                  with IDs *idx* and *idy*.
        :rtype: :class:`Node` or :class:`Edge`
        """
        try:
            if idy is None:
                # return self._nodes[idx]
                return self.find_note_by_id(idx)
            else:
                return self.edges[idx, idy]
        except IndexError:
            return None

    def find_note_by_id(self, id):
        """Return the node of a single id.

        :param int id: the id of the node
        :return: the node with ID *id*
        :rtype: :class:`Node`
        """
        for node in self._nodes:
            if node.uid is id:
                return node

    def get_pheromone_matrix(self):
        """Create pheromone matrix from the edges.

        :return: pheromone matrix
        :rtype: :class:`ndarray`
        """
        # matrix = np.zeros((len(self._nodes), len(self._nodes)), dtype=np.float)
        matrix = np.ndarray((len(self._nodes), len(self._nodes)), dtype=np.float)
        for m in self.nodes:
            for n in self.nodes:
                a, b = self.data(m), self.data(n)
                if a != b:
                    matrix[m, n] = self.data(m, n).pheromone
                else:
                    matrix[m, n] = 0.0

        return matrix

    def print_pheromone_matrix(self):
        print(pd.DataFrame(self.get_pheromone_matrix()))

    def plot_nodes(self):
        points = [pos.position for pos in self._nodes]
        plt.plot(*zip(*points), marker='o', color='r', ls='')
        plt.show()


class Edge:
    """This class represents the link between starting and ending nodes.

    In addition to *start* and *end* nodes, every :class:`Edge` has *length*
    and *pheromone* properties. *length* represents the static, *a priori*
    information, whereas *pheromone* level represents the dynamic, *a
    posteriori* information.
    
    :param node start: the node at the start of the :class:`Edge`
    :param node end: the node at the end of the :class:`Edge`
    :param float length: the length of the :class:`Edge` (default=1)
    :param float pheromone: the amount of pheromone on the :class:`Edge` 
                            (default=0.1)
    """
    # def __init__(self, start, end, length=None, pheromone=None):
    def __init__(self, start, end, lfunc, pheromone=None):
        self.start = start
        self.end = end
        self.lfunc = lfunc
        # self.length = 1 if length is None else length
        self.pheromone = 0.1 if pheromone is None else pheromone

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    @property
    def length(self):
        return self.lfunc(self.start.position, self.end.position)

    def __len__(self):
        return self.lfunc(self.start.position, self.end.position)

    def weight(self, **kwargs):
        """Calculate the weight of the edge, given alpha and beta.

        The weight of an edge is simply a representation of its perceived value
        in finding a shorter solution. Larger weights increase the odds of the
        edge being taken, whereas smaller weights decrease those odds.

        :param float alpha: the relative importance of pheromone
        :param float beta: the relative importance of distance
        :return: the weight of edge
        :rtype: float
        """
        alpha = kwargs.get('alpha', None)
        beta = kwargs.get('beta', None)

        if alpha is None:
            raise Exception('Param `alpha` is undefined')

        if beta is None:
            raise Exception('Param `beta` is undefined')

        pre = 1 / (self.length or 1)  # heuristic information
        post = self.pheromone  # pheromone information
        return post ** alpha * pre ** beta


class Node:
    """This class represents nodes.
    """
    uid = 0

    def __init__(self, position, **kwargs):
        self.uid = self.__class__.uid
        self.__class__.uid += 1
        self._position = position
        self.name = kwargs.get('name', 'node{}'.format(self.uid))
        self.description = kwargs.get('description', None)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    @property
    def position(self):
        return self._position.position


class Position:
    """This class represents the position of a node.
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    @property
    def position(self):
        return self._x, self._y
