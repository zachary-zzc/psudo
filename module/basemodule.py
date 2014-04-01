# -*- coding: utf-8 -*-

class basemodule:
    __global__ = False
    def __init__(self):
        pass

    def _var_inc(self, varName, varValue):
        if varName not in self.varList:
            self.localVarList.append(varName)
            self.varList[varName] = varValue
        # else:
        #    raise(DeclareError)

    def _func_inc(self, funcName, funcModule):
        if funcName not in self.funcList:
            self.localFuncList.append(funcName)
            self.funcList[funcName] = funcModule

    def _end_module(self):
        if not self.isGlobal():
            for key in self.localVarList:
                if key in self.varList:
                    self.varList.pop(key)
            for key in self.localFuncList:
                if key in self.funcList:
                    self.funcList.pop(key)

    def setGlobal(self):
        self.__global__ = True

    def resetGlobal(self):
        self.__global__ = False

    def isGlobal(self):
        return self.__global__

    def isEnd(self):
        return self.endRecursive

    def setEnd(self):
        self.endRecursive = True

    def resetEnd(self):
        self.endRecursive = False

    def get_localFuncList(self):
        localFuncList = {}
        for key in self.localFuncList:
            localFuncList[key] = self.funcList[key]
        return localFuncList

    def get_localVar(self):
        localVarList = {}
        for key in self.localVarList:
            localVarList[key] = self.varList[key]
        return localVarList

    def get_returnVar(self):
        returnList = []
        if '__returnList__' in self.varList:
            returnList = self.varList['__returnList__']
            self.varList.pop('__returnList__')
        return returnList


    def run(self):
        pass
