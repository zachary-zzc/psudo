# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from module.funcmodule import funcmodule

from structure.config import *
import glb
import time
import functools

SINGLETYPE = (str,
              int,
              float,
              double,
              )
ARRAYTYPE = (list,
             tuple,
             dict,
             set,
             Stack,
             Queue,
             )
TREETYPE = (Tree,)
GRAPHTYPE = ()
DIGRAPHTYPE = ()

"""
def record():
    varFile = open(r'visualize/release1.1/varList', 'w')
    for i in range(len(glb.moduleStack)):
        for varName in glb.moduleStack[i].localVarList:
            var = eval(varName, glb.moduleStack[i].varList)
            if isinstance(var, SINGLETYPE):
                var_type = 'SingleType'
            elif isinstance(var, ARRAYTYPE):
                var_type = 'ArrayType'
            elif isinstance(var, TREETYPE):
                var_type = 'TreeType'
            elif isinstance(var, GRAPHTYPE):
                var_type = 'GraphType'
            elif isinstance(var, DIGRAPHTYPE):
                var_type = 'DigraphType'
            strVar = toString(var, var_type)
            line = varName + ',' + var_type + ',' + strVar + '\n'
            varFile.write(line)
    varFile.close()

def toString(var, var_type):
    strVar = ""
    if var_type == "SingleType":
        strVar = str(var)
    elif var_type == "ArrayType":
        if len(var) > 0:
            strVar = str(var[0])
            for i in range(1, len(var)):
                strVar += ',' + str(var[i])
    elif var_type == "TreeType":
        strVar = str(var)
    elif var_type == "GraphType":
        strVar = str(var)
    elif var_type == "DiGraphType":
        strVar = str(var)
    return strVar
"""

def record_to_xml():
    from xml.dom import minidom, Node

    doc = minidom.Document()
    params = doc.createElement('Params')
    doc.appendChild(params)
    for module in glb.moduleStack:
        for varName in module.localVarList:
            var = eval(varName, module.varList)
            xmlVar = doc.createElement('var')
            xmlVar.setAttribute('name', varName)
            xmlVar.setAttribute('type', type(var).__name__)
            xmlVar.appendChild(doc.createTextNode(str(var)))
            params.appendChild(xmlVar)

    with open(r'visualize/release1.1/varList.xml', 'w') as f:
        f.write(doc.toprettyxml(indent = ''))

def refresh(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        for module in glb.moduleStack:
            for key in module.localVarList:
                outputVar = '{}: {}'.format(key, module.varList[key])
                print(outputVar)
        print('\n')
        record_to_xml()
        time.sleep(0.5)
        #input()
        return ret
    return wrapper
