# -*- coding: utf-8 -*-

import sys
import re
sys.path.append('..')

from module.funcmodule import funcmodule

from structure.config import *
import glb
import time
import functools

SINGLETYPE = (str,
              int,
              float,
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
    from copy import deepcopy
    doc = minidom.Document()
    params = doc.createElement('Params')
    doc.appendChild(params)
    for module in glb.module_stack:
        for varName in module.local_var_list:
            var = eval(varName, glb.global_var_list, module.var_list)
            xmlVar = doc.createElement('var')
            xmlVar.setAttribute('name', varName)
            xmlVar.setAttribute('type', type(var).__name__)
            tempVar=deepcopy(var)
            if hasattr(tempVar,'__iter__'):
                tempVar = tuple(tempVar)
            xmlVar.appendChild(doc.createTextNode(str(tempVar)))
            params.appendChild(xmlVar)
            for name in dir(var):
                attr=getattr(var,name)
                if(not hasattr(attr,'__call__')) and (not re.search(r'^_',name)):
                    xmlAttr=doc.createElement('attr')
                    xmlAttr.setAttribute('name',name)
                    tempAttr=deepcopy(attr)
                    if not isinstance(tempAttr, str) and hasattr(tempAttr,'__iter__'):
                        tempAttr = tuple(tempAttr)
                    xmlAttr.appendChild(doc.createTextNode(str(tempAttr)))
                    xmlVar.appendChild(xmlAttr)

    with open(r'visualize/release1.1/varList.xml', 'w') as f:
        f.write(doc.toprettyxml(indent = ''))

def refresh(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        module = func(*args, **kwargs)
        print('modules : {}'.format(glb.module_stack))
        for indx, module in enumerate(glb.module_stack):
            for key in module.local_var_list:
                outputVar = 'module : {}\n{} : {}'.format(
                        type(module),
                        key,
                        eval(key, glb.global_var_list, module.var_list))
                print(outputVar)
        print('\n')
        record_to_xml()
        time.sleep(0.1)
        #input()
        return module
    return wrapper
