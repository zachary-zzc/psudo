# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import glb

from module.basemodule import basemodule

class formodule(basemodule):
    def __init__(self, varList, exp, content):
        self.varList = varList
        self.localVarList = []
        self.content = content
        self.exp = exp
        self.endRecursive = False
        self.continueFlag= False

    def setContinue(self):
        self.continueFlag = True

    def resetContinue(self):
        self.continueFlag = False

    def run(self):
        from utils.recursive import recursive, execute
        glb.moduleStack.append(self)

        iterVarName = self.exp[0]
        for value in self.exp[1]:
            # self.localVarList.append(iterVarName)
            self.varList[iterVarName] = value
            recursive(self.content, 0, self)
            if self.continueFlag:
                self.resetEnd()
                self.resetContinue()
        self.varList.pop(iterVarName)
        self._end_module()
        glb.moduleStack.pop()
