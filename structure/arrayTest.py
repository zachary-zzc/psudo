# -*- coding: utf-8 -*-

import unittest

from myArray import myArray

class arrayTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.arr1 = myArray()
        self.arr2 = myArray([1, 2, 3])

    @classmethod
    def tearDownClass(self):
        self.arr1 = None
        self.arr2 = None

    def test_str(self):
        self.assertTrue(str(self.arr1) == '[]')
        self.assertTrue(str(self.arr2) == '[1, 2, 3]')

    def test_iterAndNext(self):
        """This function sucks, should be fixed later"""
        try:
            for item in self.arr2:
                print(item)
        except RuntimeError:
            print('array iter and next false')

    def test_len(self):
        self.assertTrue(len(self.arr1) == 0)
        self.assertTrue(len(self.arr2) == 3)

    def test_getAttr(self):
        pass

    def test_cmp(self):
        pass

    def test_insert(self):
        pass

    # Insert other tests for myArray class here


if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(arrayTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
