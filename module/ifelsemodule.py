# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from basemodule import basemodule

class ifelsemodule(basemodule):
    def __init__(self, varList, funcList, exps, contents):
        assert(len(exps) == len(contents))
        self.globalVarList = varList
        self.globalFuncList = funcList
        self.varList = {}
        self.funcList = {}
        self.exps = exps
        self.contents = contents

    def run(self):
        from utils.recursive import recursive, execute

        for i in range(len(self.exps)):
            execute('__judge__ = ' + self.exps[i], self.globalVarList, self.varList)
            if self.varList['__judge__']:
                recursive(self.contents[i], 0, self)
                break
        self._end_module()
