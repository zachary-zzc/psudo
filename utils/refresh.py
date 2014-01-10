import sys
sys.path.append('..')
import glb

import time
import functools

def printVar(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        for module in glb.moduleStack:
            for key in module.localVarList:
                outputVar = '{}: {}'.format(key, module.varList[key])
                print(outputVar)
        time.sleep(0.5)
        return ret
    return wrapper


