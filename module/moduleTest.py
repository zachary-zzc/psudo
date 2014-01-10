# -*- coding: utf-8 -*-

# unit test for modules

from commodule import commodule
from funcmodule import funcmodule
from ifelsemodule import ifelsemodule
from whilemodule import whilemodule
from formodule import formodule

import unittest

class moduleTest(unittest.TestCase):

    funcVarList = {}
    funcList = {}
    funcName = 'min'
    funcFormalParamList = ['a', 'b']
    funcActParamList = [3, 2]
    funcContent = '\tc = a + b\n\treturn c'

    varList = {'a': 1, 'b': 5, 'c':10}
    ifContent = '\tc = 10\n\tif a < b\n\t\tc = 5\n\telse\n\t\tc = 4'
    #ifContent = '\tc = 10\n\tif a == 1\n\t\te = 10'

    whileContent = '\tc = 10\n\twhile a < b\n\t\tc = b - a\n\t\ta += 1'

    forContent1 = '\tfor c = 1 to 10 step 2\n\t\tprint(c)'
    forContent2 = '\telem = 10\n\tlist = [1,2,3]\n\tfor elem in list\n\t\tprint(elem)'

    """
    def test_funcModule(self):
        content = self.funcContent.split('\n')
        funcModule = funcmodule(self.funcName, self.funcFormalParamList, content)
        funcModule.passParam(self.funcActParamList, self.funcVarList, self.funcList)
        funcModule.run()
        self.assertEqual(funcModule.get_returnVar(), 5)
    """
    """
    def test_ifModule(self):
        content = self.ifContent.split('\n')
        ifModule = commodule(self.varList, self.funcList, content)
        ifModule.run()
        self.assertEqual(ifModule.varList['c'], 5)
    """
    """
    def test_whileModule(self):
        content = self.whileContent.split('\n')
        whileModule = commodule(self.varList, self.funcList, content)
        whileModule.run()
        self.assertEqual(whileModule.varList['c'], 1)
    """
    """
    def test_forModule(self):
        content1 = self.forContent1.split('\n')
        content2 = self.forContent2.split('\n')
        forModule1 = commodule(self.varList, self.funcList, content1)
        forModule2 = commodule(self.varList, self.funcList, content2)
        forModule1.run()
        forModule2.run()
        self.assertEqual(forModule1.varList['c'], 9)
        self.assertEqual(forModule2.varList['elem'], 3)
    """

    def test_wholeModule(self):
        infile = open(r'sort', 'r')
        content = infile.readlines()
        infile.close()
        wholeModule = commodule({}, {}, content)
        wholeModule.run()
        #self.assertEqual(wholeModule.varList['d'], 5)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(moduleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
