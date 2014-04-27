# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import glb
from module.basemodule import basemodule

class funcmodule(basemodule):

    __name__ = 'FunctionModule'

    def __init__(self, func_name, param_list, content):
        self.func_name = func_name
        self.var_list = {}
        self.func_list = {}
        self.local_var_list = []
        self.content = content
        self.param_list = param_list
        self.end_recursive = False
        self.return_list = None

    def _end_module(self):
        self.var_list = {}
        self.func_list = {}
        self.local_var_list = []
        self.end_recursive = False
        self.return_list = None

        glb.module_stack.pop()


    def __call__(self, *args, **kwargs):
        from utils.recursive import recursive
        glb.module_stack.append(self)

        try:
            if not (len(args) + len(kwargs)) == len(self.param_list):
                raise(TypeError('{} positional arguments but {} given').format(
                                                    len(self.param_list),
                                                    len(args) + len(kwargs)))
            else:
                # register function formal param list
                # temp and brutial method
                # maybe should set up params when init function module
                from itertools import zip_longest
                args = list(args) + list(kwargs.values())
                for param, arg in zip_longest(self.param_list, args):
                    self.var_list[param] = arg
                    self.local_var_list.append(param)

                recursive(self.content, 0, self)

                return self.return_list

        except TypeError as e:
            print('TypeError: {}() take {}'.format(self.func_name, e))
            sys.exit(1)
        finally:
            self._end_module()

