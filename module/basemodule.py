# -*- coding: utf-8 -*-

class basemodule:

    def __init__(self, varList, funcList, content):
        self.globalVarList = varList
        self.globalfuncList = funcList
        self.varList = {}
        self.funcList = {}
        self.content = content

    def _var_inc(self, varName, varValue):
        if (varName not in self.varList and
            varName not in self.globalVarList):
            self.varList[varName] = varValue
        # else:
        #    raise(DeclareError)

    def _func_inc(self, funcName, funcModule):
        if (funcName not in self.funcList or self.globalVarList):
            self.funcList[funcName] = funcModule

    def _end_module(self):
        for key in self.varList:
            if key in self.globalVarList:
                self.globalVarList.pop(key)
        for key in self.funcList:
            if key in self.globalFuncList:
                self.globalFuncList.pop(key)

    def get_localFuncList(self):
        return self.funcList

    def get_localVar(self):
        return self.varList

    def get_returnVar(self):
        returnList = self.varList['__returnList__']
        self.varList.pop('__returnList__')
        return returnList


    def run(self):
        pass
