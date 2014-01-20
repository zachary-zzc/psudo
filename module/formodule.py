# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import glb

from basemodule import basemodule

class formodule(basemodule):
    def __init__(self, varList, funcList, exp, content):
        self.varList = varList
        self.funcList = funcList
        self.localVarList = []
        self.localFuncList = []
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
        for i in range(len(self.exp[1])):
            execute(iterVarName + '=' + str(self.exp[1][i]), self)
            recursive(self.content, 0, self)
            if self.continueFlag:
                self.resetEnd()
                self.resetContinue()

        self._end_module()
        glb.moduleStack.pop()
