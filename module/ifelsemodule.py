# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import glb

from module.basemodule import basemodule

class ifelsemodule(basemodule):
    def __init__(self, varList, exps, contents):
        assert(len(exps) == len(contents))
        self.varList = varList
        self.localVarList = []
        self.exps = exps
        self.contents = contents
        self.endRecursive = False

    def run(self):
        from utils.recursive import recursive, execute
        glb.moduleStack.append(self)

        for i in range(len(self.exps)):
            execute('__judge__ = ' + self.exps[i], self)
            # assert(isinstance(self.varList['__judge__'], bool))
            if self.varList['__judge__']:
                recursive(self.contents[i], 0, self)
                break
        self._end_module()
        glb.moduleStack.pop()
