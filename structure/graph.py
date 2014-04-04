# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

class Graph():
    __name__ = 'Graph'


    def __init__(self, vexs=[], edges=[], weights=[]):
        self._graph = {}
        # params should be list type
        assert(isinstance(vexs, list))
        assert(isinstance(edges, list))
        assert(isinstance(weights, list))
        for vex in vexs:
            self._graph[vex] = [[], []]

        from itertools import zip_longest
        for edge, weight in zip_longest(edges, weights, fillvalue=1):
            self.addEdge(edge, weight)


    def __delattr__(self, name):
        self._graph.__delattr__(name)


    def __eq__(self, obj):
        if isinstance(obj, dict):
            return self._graph == obj
        elif isinstance(obj, Graph):
            return self._graph == obj._graph
        else:
            return False


    def __str__(self):
        return str(self._graph)


    __repr__ = __str__


    def __hash__(self):
        return hash(self._graph)


    def __len__(self):
        return len(self._graph)


    def __sizeof__(self):
        return self._graph.__sizeof__()


    def vexs(self):
        for vex in self._graph.keys():
            yield vex


    def edges(self, withWeight=False):
        for vex, adjvexs in self._graph.items():
            from itertools import zip_longest
            for adjvex, weight in zip_longest(adjvexs[0], adjvexs[1]):
                if withWeight:
                    yield [vex, adjvex], weight
                else:
                    yield [vex, adjvex]


    def itervexs(self, withWeight=False):
        for vex, adjvexs in self._graph.items():
            if withWeight:
                yield vex, adjvexs[0], adjvexs[1]
            else:
                yield vex, adjvexs[0]


    def getAjacentList(self, vex, withWeight=False):
        try:
            if withWeight:
                return tuple(self._graph[vex])
            else:
                return tuple(self._graph[vex][0])
        except KeyError:
            print('vertex name {} cannot be found in this graph'.format(vex))


    def getWeight(self, edge):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not self.checkEdge(edge):
                raise KeyError
            edgeIndx = self._graph[vex1][0].index(vex2)
            return self._graph[vex1][1][edgeIndx]
        except KeyError as e:
            print(e, 'edge {} cannot be found in this graph'.format(edge))


    def setWeight(self, edge, weight):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not (self.checkEdge([vex1, vex2]) and
                    self.checkEdge([vex2, vex1])):
                raise KeyError
            edgeIndx1 = self._graph[vex1][0].index(vex2)
            self._graph[vex1][1][edgeIndx1] = weight
            edgeIndx2 = self._graph[vex2][0].index(vex1)
            self._graph[vex2][1][edgeIndx2] = weight
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
            return (vex2 in self._graph[vex1][0])
        except NameError as e:
            print(e, 'edge illegal, vertex cannot be found in this graph')


    def addEdge(self, edge, weight=1):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if (self.checkEdge([vex1, vex2])) or (self.checkEdge([vex2, vex1])):
                raise KeyError
            self._graph[vex1][0].append(vex2)
            self._graph[vex1][1].append(weight)
            self._graph[vex2][0].append(vex1)
            self._graph[vex2][1].append(weight)
        except KeyError as e:
            print(e, 'edge {} already in this graph'.format(edge))


    def delEdge(self, edge):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not ((self.checkEdge([vex1, vex2])) and
                    (self.checkEdge([vex2, vex1]))):
                raise KeyError
            adjIndx = self._graph[vex1][0].index(vex2)
            self._graph[vex1][0].pop(adjIndx)
            self._graph[vex1][1].pop(adjIndx)
            adjIndx = self._graph[vex2][0].index(vex1)
            self._graph[vex2][0].pop(adjIndx)
            self._graph[vex2][1].pop(adjIndx)
        except KeyError as e:
            print(e, 'edge {} cannot be found in this graph'.format(edge))


    def addVex(self, vex):
        try:
            if vex in self._graph:
                raise NameError
            self._graph[vex] = [[], []]
        except NameError as e:
            print(e, 'vertex {} already in this graph'.format(vex))


    def delVex(self, vex):
        try:
            if vex not in self._graph:
                raise NameError
            self._graph.pop(vex)
            for edge in self._graph.values():
                while vex in edge[0]:
                    edgeIndx = edge[0].index(vex)
                    edge[0].pop(edgeIndx)
                    edge[1].pop(edgeIndx)
        except NameError as e:
            print(e, 'vertex {} cannot be found in this graph'.format(vex))
