# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from basemodule import basemodule

class formodule(basemodule):
    def __init__(self, varList, funcList, exp, content):
        self.globalVarList = varList
        self.globalFuncList = funcList
        self.varList = {}
        self.funcList = {}
        self.content = content
        self.exp = exp

    def run(self):
        from utils.recursive import recursive, execute

        iterVarName = self.exp[0]
        for i in range(len(self.exp[1])):
            execute(iterVarName + '=' + str(self.exp[1][i]),
                 self.globalVarList,
                 self.varList)
            recursive(self.content, 0, self)

        self._end_module()
