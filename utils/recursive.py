# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from ifelsemodule import ifelsemodule
from formodule import formodule
from whilemodule import whilemodule
from funcmodule import funcmodule

import utils.parser as parser
import glb

def recursive(content, index, module):
    """
    recursively execute sentences

    Grammer structure:
    Defination: Define variables or functions, because the character of psudocode,
                assignment statement are also considered as defination

    Expression: Operations

    Statement: Including if, while, for and repeat/until, break, continue, return.
    """

    if index < len(content):
        # preprocess should remove all annotations and useless whitespaces as well as blank lines
        grammType, tokens, extoken, paramList = parser.parse(content[index], module)
        #----------DEFINATION---------
        if grammType == 'defination':
            if tokens[0][1] == 'function':
                count = getModuleIndx(content, index)
                moduleContent = [content[index+i] for i in range(1, count)]
                funcName = paramList[0]
                formalParamList = paramList[1]
                funcModule = funcmodule(funcName, formalParamList, moduleContent)
                module._func_inc(funcName, funcModule)
                index += count
            else:
                varName = paramList[0]
                module._var_inc(varName, 0)
                execute(extoken, module.globalVarList, module.varList)
                index += 1
        #---------EXPRESSION----------
        elif grammType == 'exp':
            execute(extoken, module.globalVarList, module.varList)
            index += 1
        #---------STATEMENT----------
        elif grammType == 'statement':
            # continue, break, and return
            if tokens[0][1] == 'return':
                execute('__returnList__ = '+extoken, module.globalVarList, module.varList)
                    # else:
                    #     raise VarNotDefinedError
                return
            if tokens[0][1] == 'continue':
                pass
            if tokens[0][1] == 'break':
                pass
            # if, while, and for
            count = getModuleIndx(content, index)
            moduleContent = [content[index+i] for i in range(1, count)]
            exp = paramList[0]

            if tokens[0][1] == 'if':
                exps = [exp]
                contents = [moduleContent]
                index += count
                if index < len(content):
                    grammType, tokens, extoken, paramList = parser.parse(content[index],
                                                                         module)
                    while tokens[0][1] == 'else':
                        count = getModuleIndx(content, index)
                        contents.append([content[index+1] for i in range(1, count)])
                        index += count
                        exp = paramList[0]
                        exps.append(exp)
                        if index >= len(content):
                            break
                        grammType, tokens, extoken, paramList = parser.parse(content[index],
                                                                             module)
                module.globalVarList.update(module.varList)
                module.globalFuncList.update(module.funcList)
                ifModule = ifelsemodule(module.globalVarList,
                                        module.globalFuncList,
                                        exps,
                                        contents)
                ifModule.run()
                index -= count

            elif tokens[0][1] == 'for':
                module.globalVarList.update(module.varList)
                module.globalFuncList.update(module.funcList)
                forModule = formodule(module.globalVarList,
                                      module.globalFuncList,
                                      exp,
                                      moduleContent)
                forModule.run()

            elif tokens[0][1] == 'while':
                module.globalVarList.update(module.varList)
                module.globalFuncList.update(module.funcList)
                whileModule = whilemodule(module.globalVarList,
                                          module.globalFuncList,
                                          exp,
                                          moduleContent)
                whileModule.run()
            # elif tokens[0][1] == 'repeat':
            #     pass

            index += count
        recursive(content, index, module)

def getModuleIndx(content, index):
    count = 1
    while index+count < len(content):
        indxInd = len(content[index]) - len(content[index].lstrip())
        countInd = len(content[index+count]) - len(content[index+count].lstrip())
        if countInd > indxInd:
            count += 1
        else:
            break
    return count

def execute(extoken, globalVarList, localVarList):
    # due to exec mechanism
    localVarList_bak = {}
    localVarList_bak.update(localVarList)
    exec(extoken, globalVarList, localVarList)
    # syn
    keys = []
    for key in localVarList.keys():
        if (key not in localVarList_bak) and (key in globalVarList):
            keys.append(key)
    for key in keys:
        globalVarList[key] = localVarList[key]
        localVarList.pop(key)
    if '__builtins__' in globalVarList:
        globalVarList.pop('__builtins__')
