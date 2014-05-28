# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import glb

from module.basemodule import basemodule

class whilemodule(basemodule):

    __name__ = 'WhileModule'

    def __init__(self, var_list, func_list, exp, content,line):
        """
        """
        self.var_list = var_list
        self.func_list = func_list
        self.local_var_list = []
        self.exp = exp
        self.content = content
        self._judge = False
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

        self._judge = eval(self.exp, self.var_list, glb.global_var_list)
        while self._judge:
            recursive(self.content, 0, self)
            self._judge = eval(self.exp, self.var_list, glb.global_var_list)
            if self.continue_flag:
                self.resetEnd()
                self.resetContinue()

        self._end_module()
