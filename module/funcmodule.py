# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import glb
from module.basemodule import basemodule

class funcmodule(basemodule):

    def __init__(self, func_name, param_list, content):
        self.func_name = func_name
        self.varList = {}
        self.localVarList = []
        self.content = content
        self.param_list = param_list
        self.endRecursive = False
        self.return_list = []

    """
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
    """

    def __call__(self, *args, **kwargs):
        from utils.recursive import recursive

        # register function params
        try:
            if not (len(args) + len(kwargs)) == len(self.param_list):
                raise(TypeError('{} positional arguments but {} given').format(
                                                    len(self.param_list),
                                                    len(args) + len(kwargs)))
            else:
                from itertools import zip_longest
                args = list(args) + list(kwargs.values())
                for param, arg in zip_longest(self.param_list, args):
                    self.varList[param] = arg
                    # don't know if it is possible...consider formal params as local variable
                    self.localVarList.append(param)

                recursive(self.content, 0, self)
                self._end_module()

                glb.moduleStack.pop()

                return tuple(self.return_list)
        except TypeError as e:
            print('TypeError: {}() take {}'.format(self.func_name, e))
            sys.exit(1)
