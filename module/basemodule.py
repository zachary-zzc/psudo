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

    def _var_inc(self, var_name, var_value):
        try:
            if var_name not in self.var_list:
                self.local_var_list.append(var_name)
                self.var_list[var_name] = var_value
            else:
                raise NameError
        except NameError as e:
            print('NameError: variable name \'{}\' already exist, conflict defination'.format(var_name))
            sys.exit(1)

    def _func_inc(self, func_name, func_module):
        try:
            if func_name not in self.var_list:
                # need to save function in this module
                # register function in var_list for easy python function call
                self.func_list[func_name] = func_module
                self.var_list[func_name] = \
                    lambda *args, **kwargs: self.func_list[func_name].__call__(*args, **kwargs)
            else:
                raise NameError
        except NameError as e:
            print('NameError: function name \'{}\' already exist, conflect definition'.format(func_name))
            sys.exit(1)


    def _end_module(self):
         for key in self.local_var_list:
             if key in self.var_list:
                 self.var_list.pop(key)
         # brute fix function register bugs...
         # for key in self.func_list.keys():
         #     self.var_list.pop(key)

         glb.module_stack.pop()


    def setEnd(self):
        self.end_recursive = True


    def resetEnd(self):
        self.end_recursive = False


    def run(self):
        pass
