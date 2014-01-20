# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import glb

from basemodule import basemodule

class whilemodule(basemodule):
    def __init__(self, varList, funcList, exp, content):
        """
        varList:    Vars from last module
        exp:        Tokens stand for expression
        content:    Loop content
        """
        self.varList = varList
        self.funcList = funcList
        self.localVarList = []
        self.localFuncList = []
        self.exp = exp
        self.content = content
        self.endRecursive = False
        self.continueFlag = False

    def setContinue(self):
        self.continueFlag = True

    def resetContinue(self):
        self.continueFalg = False

    def run(self):
        from utils.recursive import recursive, execute
        glb.moduleStack.append(self)

        execute('__judge__ = ' + self.exp, self)
        while self.varList['__judge__']:
            recursive(self.content, 0, self)
            execute('__judge__ = ' + self.exp, self)
            if self.continueFlag:
                self.resetEnd()
                self.resetContinue()
        self._end_module()
        glb.moduleStack.pop()
