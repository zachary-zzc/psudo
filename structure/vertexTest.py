# -*- coding: utf-8 -*-

from graph import Vertex

import unittest

class vertexTest(unittest.TestCase):

    def setUp(self):
        self.vex = Vertex('vex', ['vex0', 'vex1'])

    def tearDown(self):
        self.vex = None

    def test_eq(self):
        self.assertTrue(self.vex == 'vex')
        self.assertTrue(self.vex == Vertex('vex', ['vex1', 'vex2'], [10, 11]))

    def test_addAdj(self):
        for i in range(2):
            self.vex.addAdj('vex' + str(i+2))
        self.assertTrue(str(self.vex) == "[vex, ['vex0', 'vex1', 'vex2', 'vex3'], [1, 1, 1, 1]]")
        self.assertTrue(len(self.vex) == 4)

    def test_iter(self):
        for ind, v in enumerate(self.vex):
            self.assertTrue(v[0] == 'vex' + str(ind))
            self.assertTrue(v[1] == 1)


    def test_getitem(self):
        self.assertTrue(self.vex[1] == ('vex1', 1))


    def test_value(self):
        self.assertTrue(self.vex.value == 'vex')
        self.vex.value = 'haha'
        self.assertTrue(self.vex.value == 'haha')


    def test_delAdj(self):
        self.vex.delAdj('vex0')
        self.assertTrue(str(self.vex) == "[vex, ['vex1'], [1]]")
        self.assertTrue(len(self.vex) == 1)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(vertexTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
