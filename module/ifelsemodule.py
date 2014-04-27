# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import glb

from module.basemodule import basemodule

class ifelsemodule(basemodule):

    __name__ = 'IfElseModule'

    def __init__(self, var_list, func_list, exps, contents):
        assert(len(exps) == len(contents))
        self.var_list = var_list
        self.func_list = func_list
        # self.localVarList = []
        self.exps = exps
        self.contents = contents
        self.end_recursive = False

    def run(self):
        from utils.recursive import recursive, execute
        glb.module_stack.append(self)

        for i in range(len(self.exps)):
            execute('__judge__ = ' + self.exps[i], self)
            # assert(isinstance(self.var_list['__judge__'], bool))
            if self.var_list['__judge__']:
                recursive(self.contents[i], 0, self)
                break

        self._end_module()
