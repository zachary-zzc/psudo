# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import utils.recursive as recursive

from basemodule import basemodule

class commodule(basemodule):

    def __init__(self, varList, funcList, content):
        self.globalVarList = varList
        self.globalFuncList = funcList
        self.varList = {}
        self.funcList = {}
        self.content = content
        self.returnList = []

    def run(self):
        recursive.recursive(self.content, 0, self)
