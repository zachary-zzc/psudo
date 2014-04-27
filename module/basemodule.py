# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import glb

class basemodule:
    """
    basic module, all other modules(including loop module, branch module and function module)
    are derived from this module.

    Attributions:
        var_list: similiar to locals()

        func_list: save function contents, also registered in var_list as a lambda function which
                   will call function's __call__ method.

        end_recursive: stop running this module if True, for "return", "break" statements

        continue_flag: for "continue" statemet

    methods:
        _var_inc: register variable

        _func_inc: register function

        _end_module: deal with "tear up" staff

        setEnd: set end_recursive flag to True

        resetEnd: set end_recursive flag to False

        run: overwrite this method in each derived module
    """
    __name__ = 'BaseModule'

    def __init__(self):
        pass

    def _var_inc(self, varName, varValue):
        try:
            if varName not in self.var_list:
                # self.localVarList.append(varName)
                self.var_list[varName] = varValue
            else:
                raise NameError
        except NameError as e:
            print('NameError: variable name \'{}\' already exist, conflict defination'.format(varName))
            sys.exit(1)

    def _func_inc(self, funcName, funcModule):
        try:
            if funcName not in self.var_list:
                # need to save function in this module
                # register function in var_list for easy python function call
                self.func_list[funcName] = funcModule
                # self.localVarList.append(funcName)
                self.var_list[funcName] = \
                    lambda *args, **kwargs: self.func_list[funcName].__call__(*args, **kwargs)
            else:
                raise NameError
        except NameError as e:
            print('NameError: function name \'{}\' already exist, conflect definition'.format(funcName))
            sys.exit(1)


    def _end_module(self):
         # for key in self.localVarList:
         #     if key in self.var_list:
         #         self.var_list.pop(key)
         glb.module_stack.pop()


    def setEnd(self):
        self.end_recursive = True


    def resetEnd(self):
        self.end_recursive = False


    """
    def get_localFuncList(self):
        localFuncList = {}
        for key in self.localFuncList:
            localFuncList[key] = self.funcList[key]
        return localFuncList

    def get_localVar(self):
        localVarList = {}
        for key in self.localVarList:
            localVarList[key] = self.var_list[key]
        return localVarList
    """

    def run(self):
        pass
