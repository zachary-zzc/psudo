# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import glb

class basemodule:
    __name__ = 'BaseModule'

    def __init__(self):
        pass

    def _var_inc(self, varName, varValue):
        try:
            if varName not in self.varList:
                self.localVarList.append(varName)
                self.varList[varName] = varValue
            else:
                raise NameError
        except NameError as e:
            print('NameError: variable name \'{}\' already exist, conflict defination'.format(varName))
            sys.exit(1)

    def _func_inc(self, funcName, funcModule):
        try:
            if funcName not in self.funcList:
                self.localFuncList.append(funcName)
                self.funcList[funcName] = funcModule
            else:
                raise NameError
        except NameError as e:
            print('NameError: function name \'{}\' already exist, conflect definition'.format(funcName))
            sys.exit(1)


    def _end_module(self):
        for key in self.localVarList:
            if key in self.varList:
                self.varList.pop(key)
        for key in self.localFuncList:
            if key in self.funcList:
                self.funcList.pop(key)

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

    def run(self):
        pass
