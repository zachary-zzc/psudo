# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import glb
from module.basemodule import basemodule

class funcmodule(basemodule):

    def __init__(self, funcName, formalParamList, content):
        self.varList = {}
        self.funcName = funcName
        self.content = content
        self.formalParamList = formalParamList
        self.endRecursive = False
        self.hasVarList = True

    def get_FuncName(self):
        return self.funcName

    def passParam(self, actParamList, funcList):
        glb.moduleStack.append(self)
        # print('act param list : {}'.format(actParamList))
        # print('formal param list : {}'.format(self.formalParamList))
        self.funcList = funcList
        self.localVarList = []
        self.localFuncList = []
        assert(len(actParamList) == len(self.formalParamList))
        for i in range(len(actParamList)):
            self.varList[self.formalParamList[i]] = actParamList[i]

    def run(self):
        from utils.recursive import recursive

        recursive(self.content, 0, self)
        # for formalParam in self.formalParamList:
        #     self.varList.pop(formalParam)
        self._end_module()

        glb.moduleStack.pop()
