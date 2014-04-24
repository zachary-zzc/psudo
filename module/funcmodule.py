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
        self.returnList = []

    def get_FuncName(self):
        return self.funcName

    def passParam(self, actParamList, funcList):
        glb.moduleStack.append(self)
        self.funcList = funcList
        self.localVarList = []
        self.localFuncList = []
        assert(len(actParamList) == len(self.formalParamList))
        for i in range(len(actParamList)):
            self.varList[self.formalParamList[i]] = actParamList[i]

    def getReturnList(self):
        return tuple(self.returnList)

    def run(self):
        from utils.recursive import recursive

        # one line can only deliver one function... should be fixed later
        glb.globalVarList['__return__'] = None
        recursive(self.content, 0, self)
        for formalParam in self.formalParamList:
            self.localVarList.append(formalParam)
        # for formalParam in self.formalParamList:
        #     self.varList.pop(formalParam)
        self._end_module()

        glb.moduleStack.pop()
