# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from itertools import zip_longest

class Vertex():
    __name__ = 'Vertex'
    def __init__(self, val, adjs=[], weights=[]):
        if isinstance(val, Vertex):
            self._value = val._value
            self._adjs = val._adjs
            self._weights = val._weights
            self._color = val._color
            self._pi = val._pi
        else:
            self._value = val
            self._adjs = adjs
            self._weights = [1] * len(adjs)
            # used in BFS
            self._color = 'white'
            self._distance = sys.maxsize
            self._pi = None
            if len(weights) < len(adjs):
                self._weights[:len(weights)] = weights
            else:
                self._weights = weights[:len(adjs)]

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
        return '[' + str(self.value) + ']'
        #return '[' + str(self.value) + ', ' + str(self.adjs) + ', ' + str(self.weights) + ']'


    __repr__ = __str__


    def __len__(self):
        return len(self.adjs)


    def __iter__(self):
        for adj, weight in zip_longest(self.adjs, self.weights):
            yield adj, weight


    def __getitem__(self, ind):
        return self._adjs[ind], self._weights[ind]


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
    def weights(self):
        return self._weights


    @weights.setter
    def weights(self, weights):
        self._weights = weights


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


    def addAdj(self, vex, weight=1):
        try:
            if vex not in self.adjs:
                self._adjs.append(vex)
                self._weights.append(weight)
            else:
                raise KeyError
        except KeyError:
            glb.current_line
            glb.current_content
            print('vertex {} already exist in adj list'.format(vex))


    def delAdj(self, vex):
        try:
            if vex in self.adjs:
                indx = self._adjs.index(vex)
                self._adjs.pop(indx)
                self._weights.pop(indx)
            else:
                raise KeyError
        except KeyError:
            print('vertex {} cannot be found in adj list'.format(vex))



class Graph():
    __name__ = 'Graph'


    def __init__(self, vexs=[], edges=[], weights=[]):
        self._graph = set([Vertex(value, [], []) for value in vexs])

        # weights should not longer than edges
        if len(weights) > len(edges):
            weights = weights[:len(edges)]
        for edge, weight in zip_longest(edges, weights, fillvalue=1):
            self.addEdge(edge, weight)


    def __delattr__(self, name):
        self._graph.__delattr__(name)


    def __eq__(self, obj):
        if isinstance(obj, Graph):
            return self._graph == obj._graph
        else:
            return False


    def __str__(self):
        """
        use adj_matrix format for conv use
        format:
            fst row: list of all vex name
            sec row: adj_matrix
        
        import numpy as np
        ret = '['
        vex_list = [vex.value for vex in self.vexs()]
        adj_matrix = np.ones((len(vex_list), len(vex_list))) * -1
        for ind, vex in enumerate(self.vexs()):
            for adj, weight in zip_longest(vex.adjs, vex.weights):
                adj_matrix[ind][vex_list.index(adj)] = weight
        ret += str(vex_list) + ', \n' + str(adj_matrix) + ']'
        return ret
        """
        
        ret='('
        for vex in  self.vexs():
            ret+= '[' + str(vex.value) + ', ' + str(vex.adjs) + ', ' + str(vex.weights) + ']'+','
        ret=ret[:-1]
        ret+=')'
        return ret
        #return str(list(self._graph))

    __repr__ = __str__


    def __hash__(self):
        return hash(self._graph)


    def __len__(self):
        return len(self._graph)


    def __sizeof__(self):
        return self._graph.__sizeof__()


    @property
    def V(self):
        return list(self.vexs())


    def vexs(self):
        for vex in self._graph:
            yield vex

    @property
    def E(self):
        return list(self.edges())


    def edges(self):
        edges = []
        for vex in self.vexs():
            for adj in vex.adjs:
                if isinstance(vex.adjs, Vertex):
                    edges.append((vex.value, adj.value))
                else:
                    edges.append((vex.value, adj))
        for edge in set(edges):
            yield edge



    def getVertex(self, vex):
        try:
            if vex in self._graph:
                for v in self._graph:
                    if v.value == vex:
                        return v
            else:
                raise KeyError
        except KeyError:
            print('vertex {} cannot be found in this graph'.format(vex))



    def getAdjs(self, vex):
        return tuple(list(map(self.getVertex, self.getVertex(vex).adjs)))



    def getWeight(self, edge):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not self.checkEdge(edge):
                raise KeyError
            edgeIndx = self.getAdjs(vex1).index(vex2)
            return self.getVertex(vex1).weights[edgeIndx]
        except KeyError as e:
            print(e, 'edge {} cannot be found in this graph'.format(edge))


    def setWeight(self, edge, weight):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not (self.checkEdge([vex1, vex2]) and
                    self.checkEdge([vex2, vex1])):
                raise KeyError
            edgeIndx1 = self.getAdjs(vex1).index(vex2)
            self.getVertex(vex1).weights[edgeIndx1] = weight
            edgeIndx2 = self.getAdjs(vex2).index(vex1)
            self.getVertex(vex2).weights[edgeIndx2] = weight
        except KeyError as e:
            print(e, 'edge {} cannot be found in this graph'.format(edge))


    def checkVex(self, vex):
        return (vex in self._graph)


    def checkEdge(self, edge):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not ((self.checkVex(vex1)) and (self.checkVex(vex2))):
                raise NameError
            return (vex2 in self.getAdjs(vex1))
        except NameError as e:
            print(e, 'edge illegal, vertex cannot be found in this graph')


    def addEdge(self, edge, weight=1):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if (self.checkEdge([vex1, vex2])) or (self.checkEdge([vex2, vex1])):
                raise KeyError
            self.getVertex(vex1).addAdj(vex2, weight)
            self.getVertex(vex2).addAdj(vex1, weight)
        except KeyError as e:
            print(e, 'edge {} already in this graph'.format(edge))


    def delEdge(self, edge):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not ((self.checkEdge([vex1, vex2])) and
                    (self.checkEdge([vex2, vex1]))):
                raise KeyError
            self.getVertex(vex1).delAdj(vex2)
            self.getVertex(vex2).delAdj(vex1)
        except KeyError as e:
            print(e, 'edge {} cannot be found in this graph'.format(edge))


    def addVertex(self, vex):
        try:
            if vex in self._graph:
                raise NameError
            self._graph.update({Vertex(vex, [], [])})
        except NameError as e:
            print(e, 'vertex {} already in this graph'.format(vex))


    def delVertex(self, vex):
        try:
            if vex not in self._graph:
                raise NameError
            self._graph = self._graph - {vex}
            for v in self._graph:
                if vex in v.adjs:
                    v.delAdj(vex)
        except NameError as e:
            print(e, 'vertex {} cannot be found in this graph'.format(vex))
