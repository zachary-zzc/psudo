# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import glb

from module.basemodule import basemodule

class commodule(basemodule):

    def __init__(self, varList, content):
        self.varList = varList
        self.localVarList = []
        self.content = content
        self.endRecursive = False

    def run(self):
        import utils.recursive as recursive
        glb.moduleStack.append(self)

        recursive.recursive(self.content, 0, self)
        glb.moduleStack.pop()
