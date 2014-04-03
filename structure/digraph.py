# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from structure.graph import Graph

class DiGraph(Graph):
    __name__ = 'DiGraph'
    __class__ = 'DiGraph'


    def getTailList(self, vex, withWeight=False):
        return self.getAjacentList(vex, withWeight)


    def getHeadList(self, vex, withWeight=False):
        headList = []
        weightList = []
        try:
            if vex not in self._graph:
                raise NameError
            for v, e in self._graph.items():
                if vex in e[0]:
                    headList.append(v)
                    weightList.append(e[1][e[0].index(vex)])
            if withWeight:
                return tuple([headList, weightList])
            else:
                return tuple(headList)
        except NameError as e:
            print('vertex name {} cannot be found in this graph'.format(vex))


    def setWeight(self, edge, weight):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not self.checkEdge(edge):
                raise KeyError
            edgeIndx = self._graph[vex1][0].index(vex2)
            self._graph[vex1][1][edgeIndx] = weight
        except KeyError as e:
            print(e, 'edge {} cannot be found in this graph'.format(edge))


    def addEdge(self, edge, weight=1):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if self.checkEdge(edge):
                raise KeyError
            self._graph[vex1][0].append(vex2)
            self._graph[vex1][1].append(weight)
        except KeyError as e:
            print(e, 'edge {} already in this graph'.format(edge))


    def delEdge(self, edge):
        assert(len(edge) == 2)
        vex1, vex2 = edge
        try:
            if not self.checkEdge(edge):
                raise KeyError
            edgeIndx = self._graph[vex1][0].index(vex2)
            self._graph[vex1][0].pop(edgeIndx)
            self._graph[vex1][1].pop(edgeIndx)
        except KeyError as e:
            print(e, 'edge {} cannot be found in this graph'.format(edge))

