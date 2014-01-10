# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from basemodule import basemodule

class funcmodule(basemodule):

    def __init__(self, funcName, formalParamList, content):
        self.funcName = funcName
        self.content = content
        self.formalParamList = formalParamList

    def passParam(self, actParamList, varList, funcList):
        self.globalVarList = varList
        self.globalFuncList = funcList
        self.varList = {}
        self.funcList = {}
        assert(len(actParamList) == len(self.formalParamList))
        for i in range(len(actParamList)):
            self.varList[self.formalParamList[i]] = actParamList[i]

    def run(self):
        from utils.recursive import recursive
        recursive(self.content, 0, self)
        for formalParam in self.formalParamList:
            self.varList.pop(formalParam)
        self._end_module()
