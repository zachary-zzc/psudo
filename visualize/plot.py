# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from module.funcmodule import funcmodule

import structure
import glb
import time
import functools

from PIL import Image

SINGLETYPE = (str,
              int,
              )
ARRAYTYPE = (list,
             tuple,
             dict,
             set, )
TREETYPE = ()
GRAPHTYPE = ()
DIGRAPHTYPE = ()

def plot():
    varFile = open(r'varList.txt', 'w')
    for i in range(len(glb.moduleStack)):
        for varName in glb.moduleStack[i].localVarList:
            var = eval(varName, glb.moduleStack[i].varList)
            if isinstance(var, SINGLETYPE):
                var_type = 'single'
            elif isinstance(var, ARRAYTYPE):
                var_type = 'array'
            elif isinstance(var, TREETYPE):
                var_type = 'tree'
            elif isinstance(var, GRAPHTYPE):
                var_type = 'graph'
            elif isinstance(var, DIGRAPHTYPE):
                var_type = 'digraph'
            line = varName + ', ' + var_type + ', ' + str(var) + '\n'
            varFile.write(line)
    varFile.close()

def refresh(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print('\n')
        for module in glb.moduleStack:
            for key in module.localVarList:
                outputVar = '{}: {}'.format(key, module.varList[key])
                print(outputVar)
        print('\n')
        plot()
        time.sleep(0.5)
        #input()
        return ret
    return wrapper
