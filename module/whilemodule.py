# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from basemodule import basemodule

class whilemodule(basemodule):
    def __init__(self, varList, funcList, exp, content):
        """
        varList:    Vars from last module
        exp:        Tokens stand for expression
        content:    Loop content
        """
        self.globalVarList = varList
        self.globalFuncList = funcList
        self.varList = {}
        self.funcList = {}
        self.exp = exp
        self.content = content

    def run(self):
        from utils.recursive import recursive, execute

        execute('__judge__ = ' + self.exp, self.globalVarList, self.varList)
        while self.varList['__judge__']:
            recursive(self.content, 0, self)
            execute('__judge__ = ' + self.exp, self.globalVarList, self.varList)
        self.varList.pop('__judge__')

        self._end_module()
