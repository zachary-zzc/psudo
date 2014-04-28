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
        self.param_list = param_list
        self.content = content
        self.end_recursive = False
        self.return_list = None


    @staticmethod
    def function_factory(obj):
        ret = funcmodule(obj.func_name, obj.param_list, obj.content)
        return ret


    def __call__(self, *args, **kwargs):
        """
        __call__ function will actually exec a copy of this funcmodule, to void
        recursive function call error
        """
        from utils.recursive import recursive

        function = funcmodule.function_factory(self)

        glb.module_stack.append(function)

        try:
            if not (len(args) + len(kwargs)) == len(function.param_list):
                raise(TypeError('{} positional arguments but {} given'.format(
                                                    len(function.param_list),
                                                    len(args) + len(kwargs))))
            else:
                # register function formal param list
                # temp and brutial method
                # maybe should set up params when init function module
                from itertools import zip_longest
                args = list(args) + list(kwargs.values())
                for param, arg in zip_longest(function.param_list, args):
                    function.var_list[param] = arg
                    function.local_var_list.append(param)

                recursive(function.content, 0, function)

                return function.return_list

        except TypeError as e:
            print('TypeError: {}() take {}'.format(function.func_name, e))
            sys.exit(1)
        finally:
            function._end_module()

