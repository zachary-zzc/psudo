# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import glb

from module.basemodule import basemodule

class formodule(basemodule):

    __name__ = 'ForModule'

    def __init__(self, var_list, func_list, exp, content):
        self.var_list = var_list
        self.func_list = func_list
        # self.localVarList = []
        self.content = content
        self.exp = exp
        self.end_recursive = False
        self.continue_flag= False

    def setContinue(self):
        self.continue_flag = True

    def resetContinue(self):
        self.continue_flag = False

    def run(self):
        from utils.recursive import recursive, execute
        glb.module_stack.append(self)

        iterVarName = self.exp[0]
        for value in self.exp[1]:
            # self.localVarList.append(iterVarName)
            self.var_list[iterVarName] = value
            recursive(self.content, 0, self)
            if self.continue_flag:
                self.resetEnd()
                self.resetContinue()
        self.var_list.pop(iterVarName)

        self._end_module()
