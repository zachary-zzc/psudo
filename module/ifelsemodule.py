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
        self.local_var_list = []
        self.exps = exps
        self.contents = contents
        self.end_recursive = False

    def run(self):
        from utils.recursive import recursive, execute
        glb.module_stack.append(self)

        from itertools import zip_longest
        for exp, content in zip_longest(self.exps, self.contents):
            execute('__judge__ = ' + exp, self)
            # assert(isinstance(self.var_list['__judge__'], bool))
            if self.var_list['__judge__']:
                recursive(content, 0, self)
                break

        self._end_module()
