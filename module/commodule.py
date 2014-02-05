# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import glb

from module.basemodule import basemodule

class commodule(basemodule):

    def __init__(self, varList, funcList, content):
        self.varList = varList
        self.funcList = funcList
        self.localVarList = []
        self.localFuncList = []
        self.content = content
        self.returnList = []
        self.endRecursive = False

    def run(self):
        import utils.recursive as recursive
        glb.moduleStack.append(self)

        recursive.recursive(self.content, 0, self)
        glb.moduleStack.pop()
