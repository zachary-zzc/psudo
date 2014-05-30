# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from structure.graph_mod import Graph

class DiGraph(Graph):
    __name__ = 'DiGraph'


    def getTails(self, vex):
        return self.getAjds(vex)


    def getHeads(self, vex):
        """
        headList = []
        try:
            if vex in self._graph:
                for vex in self.vexs():
                    if vex in vex.adjs:

            else:
                raise NameError
        except NameError as e:
            print('vertex name {} cannot be found in this graph'.format(vex))
        """
        pass


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

