# -*- coding: utf-8 -*-

# unit test for graph structure

from graph_mod import Vertex, Graph

import unittest

class graphTest(unittest.TestCase):
    def setUp(self):
        self.graph = Graph([1, 2, 3], [(1, 2), (1, 3)], [5])

    def tearDown(self):
        self.graph = None


    def test_str(self):
        # if init success, addEdge should work OK, no need test
        print(str(self.graph))
        self.assertTrue(str(self.graph) == '[[1, [2, 3]], [2, [1]], [3, [1]]]')
        self.assertTrue(len(self.graph) == 3)


    def test_checkVex(self):
        self.assertTrue(self.graph.checkVex(2))
        self.assertTrue(not self.graph.checkVex(100))
        self.assertTrue(self.graph.checkVex(Vertex(2)))


    def test_checkEdge(self):
        self.assertTrue(self.graph.checkEdge((1, 3)))
        self.assertTrue(not self.graph.checkEdge((2, 3)))


    def test_iter(self):
        for ind, vex in enumerate(self.graph.vexs()):
            self.assertTrue(vex.value == ind+1)
            self.assertTrue(vex == ind+1)
        self.assertTrue(self.graph.V == {1, 2, 3})
        self.assertTrue(self.graph.E == {(1, 2), (1, 3)})
        for edge in self.graph.edges():
            self.assertTrue(edge in self.graph.E)


    def test_getVertex(self):
        self.assertTrue(self.graph.getVertex(1) == 1)
        self.assertTrue(type(self.graph.getVertex(1)) == Vertex)


    def test_getAdjs(self):
        self.assertTrue(self.graph.getAdjs(1) == (2, 3))


    def test_getWeight(self):
        self.assertTrue(self.graph.getWeight((1, 2)) == 5)
        print(self.graph.getWeight((1, 3)))
        self.assertTrue(self.graph.getWeight((1, 3)) == 1)


    def test_setWeight(self):
        self.graph.setWeight((1, 3), 10)
        self.assertTrue(self.graph.getWeight((1, 3)) == 10)


    def test_delEdge(self):
        print(self.graph)
        self.graph.delEdge((1, 3))
        print(self.graph)
        self.assertTrue(str(self.graph) == '[[1, [2]], [2, [1]], [3, []]]')

    def test_addVertex(self):
        self.graph.addVertex(5)
        print(self.graph._vertexs)
        self.assertTrue(self.graph.getVertex(5) == 5)
