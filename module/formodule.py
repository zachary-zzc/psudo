# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import glb

from module.basemodule import basemodule

class formodule(basemodule):

    __name__ = 'ForModule'

    def __init__(self, var_list, func_list, exp, content,line):
        self.var_list = var_list
        self.func_list = func_list
        self.local_var_list = []
        self.content = content
        self.iter_var = exp[0]
        self.loop = exp[1]
        self.end_recursive = False
        self.continue_flag = False
        self.line = line

    def setContinue(self):
        self.continue_flag = True

    def resetContinue(self):
        self.continue_flag = False

    def run(self):
        from utils.recursive import recursive, execute
        glb.module_stack.append(self)

        for value in self.loop:
            self.var_list[self.iter_var] = value
            recursive(self.content, 0, self)
            if self.continue_flag:
                self.resetEnd()
                self.resetContinue()
        self.var_list.pop(iterVarName)

        self._end_module()
