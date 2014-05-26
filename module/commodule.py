# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import glb

from module.basemodule import basemodule

class commodule(basemodule):
    """
    maybe this should be called glbmodule...
    basically is a instanced basicmodule
    """

    __name__ = 'CommonModule'

    def __init__(self, var_list, func_list, content,line):
        self.var_list = var_list
        self.func_list = func_list
        self.local_var_list = []
        self.content = content
        self.end_recursive = False
        self.line = line

    def run(self):
        import utils.recursive as recursive
        glb.module_stack.append(self)

        recursive.recursive(self.content, 0, self)

        self._end_module()
