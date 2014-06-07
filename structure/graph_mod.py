# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from itertools import zip_longest

class Vertex():
    __name__ = 'Vertex'
    def __init__(self, val, adjs=[]):
        if isinstance(val, Vertex):
            self._value = val._value
            self._adjs = val._adjs
            self._color = val._color
            self._pi = val._pi
        else:
            self._value = val
            self._adjs = adjs
            # used in BFS
            self._color = 'white'
            self._distance = sys.maxsize
            self._pi = None

    def __eq__(self, obj):
        if isinstance(obj, Vertex):
            return self.value == obj.value
        else:
            return self.value == obj


    def __cmp__(self, obj):
        if isinstance(obj, Vertex):
            return cmp(self.value, obj.value)
        else:
            return cmp(self.value, obj)

    def __lt__(self, obj):
        if isinstance(obj, Vertex):
            return self.value < obj.value
        else:
            return self.value < obj

    def __gt__(self, obj):
        if isinstance(obj, Vertex):
            return self.value > obj.value
        else:
            return self.value > obj

    def __str__(self):
        return '[' + str(self.value) + ', ' + str(self.adjs) + ']'


    __repr__ = __str__


    def __len__(self):
        return len(self.adjs)


    def __iter__(self):
        for adj in self.adjs:
            yield adj


    def __getitem__(self, ind):
        return self._adjs[ind]# , self._weights[ind]


    # stop using getslice in python3
    """def __getslice__(self, ind1, ind2):
        return tuple([(adj, weight) for adj, weight in zip_longest(self._adjs[ind1:ind2], self._weights[ind1:ind2])])
    """

    def __hash__(self):
        return hash(self._value)


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        self._value = value


    @property
    def adjs(self):
        return self._adjs


    @adjs.setter
    def adjs(self, adjs):
        self._adjs = adjs


    @property
    def color(self):
        return self._color


    @color.setter
    def color(self, color):
        self._color = color


    @property
    def distance(self):
        return self._distance


    @distance.setter
    def distance(self, distance):
        self._distance = distance


    @property
    def pi(self):
        return self._pi


    @pi.setter
    def pi(self, pi):
        self._pi = pi


    def addAdj(self, vex):
        if vex not in self.adjs:
            self._adjs.append(vex)
        else:
            raise KeyError('vertex {} already exist in adj list'.format(vex))


    def delAdj(self, vex):
        if vex in self.adjs:
            indx = self._adjs.index(vex)
            self._adjs.pop(indx)
            # self._weights.pop(indx)
        else:
            raise KeyError('vertex {} cannot be found in adj list'.format(vex))


class Edge():
    __name__ = 'Edge'

    def __init__(self, pair, weight=None, ordered=False):
        assert(len(pair) == 2)
        self._pair = tuple(pair)
        self._weight = weight or 1
        self._ordered = False


    def __str__(self):
        return str(self._pair)


    __repr__ = __str__


    def __cmp__(self, obj):
        return cmp(self._pair, obj._pair)


    def __eq__(self, obj):
        if isinstance(obj, Edge):
            return self._pair == obj._pair
        else:
            return self._pair[0] == obj[0] and self._pair[1] == obj[1]


    def __hash__(self):
        return hash(self._pair)


    @property
    def start_point(self):
        return self._pair[0]


    @property
    def end_point(self):
        return self._pair[1]


    @property
    def vertex_pair(self):
        return self._pair


    @property
    def weight(self):
        return self._weight


    @weight.setter
    def weight(self, weight):
        self._weight = weight



class Graph():
    __name__ = 'Graph'


    def __init__(self, vexs=[], edges=[], weights=[]):
        assert(len(set(vexs)) == len(vexs))
        from itertools import zip_longest
        self._vertexs = [Vertex(value, []) for value in vexs]
        # self._num_vertex = vexs.__len__
        # self._num_edge = edges.__len__
        self._edges = [Edge(edge, weight, False) for edge, weight in zip_longest(edges,weights)]

        # weights should not longer than edges
        if len(weights) > len(edges):
            weights = weights[:len(edges)]
        for edge, weight in zip_longest(edges, weights, fillvalue=1):
            self.addEdge(edge, weight)


    def __delattr__(self, name):
        self._vertexs.__delattr__(name)


    def __eq__(self, obj):
        if isinstance(obj, Graph):
            return self._vertexs == obj._vertexs and self._edges == obj._edges
        else:
            return False


    def __str__(self):
        """
        """

        ret = '['
        for vex in  self.vexs():
            # ret+= '[' + str(vex.value) + ', ' + str(vex.adjs) + ', ' + str(vex.weights) + ']'+','
            ret += '[' + str(vex.value) + ', ' + str(vex.adjs) + ']'+', '
        ret = ret[:-2]
        ret += ']'
        return ret

    __repr__ = __str__


    def __hash__(self):
        return hash(self._vertexs)


    def __len__(self):
        return len(self._vertexs)


    def __sizeof__(self):
        return self._vertexs.__sizeof__()

    @property
    def vertex_count(self):
        return len(list(self.vexs()))

    @property
    def edge_count(self):
        return len(list(self.edges()))


    @property
    def V(self):
        return set(self.vexs())


    def vexs(self):
        for vex in self._vertexs:
            yield vex

    @property
    def E(self):
        return set(self.edges())


    def edges(self):
        for edge in self._edges:
            yield edge


    def getVertex(self, vex):
        return self._vertexs[self._vertexs.index(vex)]


    def getEdge(self, from_node, to_node):
        if isinstance(from_node, Node):
            from_node = from_node._value
        if isinstance(to_node, Node):
            to_node = to_node._value
        return self._edges[self._edges.index(Edge((from_node, to_node)))]


    def getAdjEdges(self, from_node):
        if isinstance(from_node):
            from_node = from_node._value
        from itertools import filterfalse
        return list(filterfalse(lambda x: from_node in x._pair, self._edges))



    def getAdjs(self, vex):
        return list(map(self.getVertex, self.getVertex(vex).adjs))






    def getWeight(self, edge):
        if edge in self._edges:
            return self._edges[self._edges.index(edge)].weight


    def setWeight(self, edge, weight):
        if edge in self._edges:
            self._edges[self._edges.index(edge)].weight = weight


    def checkVex(self, vex):
        return (vex in self._vertexs)


    def checkEdge(self, edge):
        assert(len(edge) == 2)
        vex1, vex2 = edge

        if not ((self.checkVex(vex1)) and (self.checkVex(vex2))):
            raise NameError('edge illegal, vertex cannot be found')

        return (vex2 in self.getAdjs(vex1)) and (edge in self._edges)


    def addEdge(self, edge, weight):
        assert(len(edge) == 2)
        vex1, vex2 = edge

        if (self.checkEdge([vex1, vex2])) or (self.checkEdge([vex2, vex1])):
            raise KeyError('edge {} already'.format(edge))
        self.getVertex(vex1).addAdj(vex2)
        self.getVertex(vex2).addAdj(vex1)
        self._edges.append(Edge(edge, weight))


    def delEdge(self, edge):
        assert(len(edge) == 2)

        vex1, vex2 = edge
        if not self.checkEdge((vex1, vex2)):
            raise KeyError('edge {} cannot be found'.format(edge))

        self.getVertex(vex1).delAdj(vex2)
        self.getVertex(vex2).delAdj(vex1)
        self._edges.pop(self._edges.index(edge))


    def addVertex(self, vex):
        if vex in self._vertexs:
            raise NameError('vertex {} already'.format(vex))
        self._vertexs.append(Vertex(vex, []))


    def delVertex(self, vex):
        if vex not in self._vertexs:
            raise NameError('vertex {} cannot be found'.format(vex))

        self._vertexs.pop(self._vertexs.index(vex))

        for v in self._vertexs:
            if vex in v.adjs:
                v.delAdj(vex)
        del_map = []
        for index, edge in enumerate(self._edges):
            if vex in edge.vertex_pair:
                del_map.append(index)
        map(self._edges.pop, del_map)
        self._vertexs.pop(self._vertexs.index(vex))
