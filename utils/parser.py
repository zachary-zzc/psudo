# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import string

STATEMENTRANGE = (4, 13)

keywords = {'if':       4,
            'else':     5,
            'for':      6,
            'while':    7,
            'break':    8,
            'continue': 9,
            'return':   10,
            'repeat':   11,
            'until':    12,
            'function': 13,
            'is':       14,
            'in':       15,
            'or':       16,
            'and':      17,
            'not':      18,
            'swap':     19,
            }

opts = {'+':            41,
        '-':            42,
        '*':            43,
        '/':            44,
        '<':            45,
        '<=':           46,
        '>':            47,
        '>=':           48,
        '<>':           49,
        '!=':           50,
        '=':            51,
        '==':           52,
        ';':            53,
        '(':            54,
        ')':            55,
        '&':            56,
        '&&':           57,
        '|':            58,
        '||':           59,
        '^':            60,
        '%':            61,
        '>>':           62,
        '<<':           63,
        ',':            64,
        }

def preprocess(strContent):
    orig = strContent.split('\n')
    contents = []
    for i in range(len(orig)):
        content = orig[i].rstrip()
        if '#' in content:
            content = content.split('#')[0]
        if len(content) > 0:
            contents.append(content)
    return contents



def lexical(block):
    """
    lexical analysis:
        input: sentence, e.g., 'for i = 1 to 9, step = 10'
        output: syn, token pair (syn, token) list.

        4 kinds of syn:
        1. key words:
            for, if, else, repeat, until, while, function, is, in, or, and
        2. opts:
            +, -, *, /, <, <=, >, >=, <>, !=, =, ==, ;, (, ), &, &&, ^, %, |, ||, >>, <<,
        3. var ID:
            VarName
        4. func ID:
            FuncName
        5. Constant

        syn coding table:
        VarID:      1
        FuncID:     2
        Constant    3
        Keywords    4-40
        Opts        41-
    """
    token = ''
    tokens = []
    # as python, '#' stand for annotation
    block = block.split('#')[0]

    indx = 0
    while indx < len(block):
        ch = block[indx]
        if ch == ' ' or ch == '\t' or ch == '\n':
            indx += 1
            continue
        if ch.isalpha():
            while (ch.isalpha() or ch.isdigit() or ch == '.' or ch == '_'):
                token += ch
                indx += 1
                if indx < len(block):
                    ch = block[indx]
                else:
                    break
            if ch == '(':
                while (ch != ')'):
                    token += ch
                    indx += 1
                    if indx < len(block):
                        ch = block[indx]
                    else:
                        break
                token += ch
                tokens.append((2, token))
            elif ch == '[':
                while (ch != ']'):
                    token += ch
                    indx += 1
                    if indx < len(block):
                        ch = block[indx]
                    else:
                        break
                token += ch
                tokens.append((1, token))
            else:
                indx -= 1
                if token in keywords:
                    tokens.append((keywords.get(token), token))
                else:
                    tokens.append((1, token))

        elif ch.isdigit():
            while (ch.isdigit() or ch == '.'):
                token += ch
                indx += 1
                if indx < len(block):
                    ch = block[indx]
                else:
                    break
            indx -= 1
            tokens.append((3, token))

        elif ch == '\'':
            token += ch
            indx += 1
            ch = block[indx]
            while ch != '\'':
                token += ch
                indx += 1
                if indx < len(block):
                    ch = block[indx]
                else:
                    break
            token += ch
            tokens.append((3, token))

        elif ch == '\"':
            token += ch
            indx += 1
            ch = block[indx]
            while ch != '\"':
                token += ch
                indx += 1
                if indx < len(block):
                    ch = block[indx]
                else:
                    break
            token += ch
            tokens.append((3, tokens))

        else:
            token += ch
            if ch == '<':
                indx += 1
                ch = block[indx]
                if ch == '=' or ch == '>':
                    token += ch
                else:
                    indx -= 1
            elif ch == '>':
                indx += 1
                ch = block[indx]
                if ch == '=':
                    token += ch
                else:
                    indx -= 1
            elif ch == '!':
                indx += 1
                ch = block[indx]
                if ch == '=':
                    token += ch
                else:
                    indx -= 1
            elif ch == '=':
                indx += 1
                ch = block[indx]
                if ch == '=':
                    token += ch
                else:
                    indx -= 1
            elif ch == '&':
                indx += 1
                ch = block[indx]
                if ch == '&':
                    token += ch
                else:
                    indx -= 1
            elif ch == '|':
                indx += 1
                ch = block[indx]
                if ch == '|':
                    token += ch
                else:
                    indx -= 1
            elif ch == '<':
                indx += 1
                ch = block[indx]
                if ch == '<':
                    token += ch
                else:
                    indx -= 1
            elif ch == '>':
                indx += 1
                ch = block[indx]
                if ch == '>':
                    token += ch
                else:
                    indx -= 1
            tokens.append((opts.get(token), token))
        indx += 1
        token = ''
    return tuple(tokens)

def parse(block, module):
    """
    Input: sentence, same with lexical
           funcList, for convinient use, should not appear here
    Output:
    1. grammType: 'defination', 'statement', 'exp'
    2. token: executable tokens for python, for execute function use
    3. paramList: Due to grammType.
        If block is var defination, paramList[0] = varName
        If block is function defination, paramList[0] = funcName
                                         paramList[1] = formalParamList
        if block is if or while statement, paramList[0] is there judge exp
        if block is for statement, paramList[0] is iter varName and iter list
                                   e.g 'for i = 1 to 10, step 1'
                                   paramList[0] = ('i', (1, 2, 3, ..., 10))

    for statement have two types:
        1. for [varName] in [iterableList]
        2. for [varName] = [startpos] to [endpos] step [step]
    """

    grammType = ''
    token = ''
    paramList = []
    tokens = lexical(block)

    if len(tokens) == 0:
        return

    if tokens[0][1] == 'function':
        grammType = 'defination'
        funcName, formalParamList = getFunc(tokens[1][1])
        paramList.append(funcName)
        paramList.append(formalParamList)
        token = funcName
    # if not define function, run prog defined function and replace these tokens with there return, this part sucks
    else:
        tokens = runFuncs(tokens, module)
        if tokens[0][0] == 1:
            if tokens[1][0] == 1:
                grammType = 'defination'
                varType = tokens[0][1]
                varName = tokens[1][1]
                paramList.append(varName)
                token = varName + '=' + varType
                if len(tokens) == 2:
                    token += '()'
                else:
                    if tokens[2][1] == '=':
                        token += '('
                        for indx in range(3, len(tokens)):
                            token = token + tokens[indx][1]
                        token += ')'
            # elif tokens[1][1] == '=':
            #     grammType = 'defination'
            #     varName = tokens[0][1]
            #     paramList.append(varName)
            #     for indx in range(len(tokens)):
            #         token = token + tokens[indx][1] + ' '
            else:
                grammType = 'exp'
                for indx in range(len(tokens)):
                    token = token + tokens[indx][1] + ''
        elif tokens[0][0] in range(STATEMENTRANGE[0], STATEMENTRANGE[1]):
            grammType = 'statement'
            if tokens[0][1] == 'for':
                from utils.recursive import execute
                varName = tokens[1][1]
                if tokens[2][1] == 'in':
                    if tokens[3][1] in module.varList:
                        paramList.append((varName, module.varList[tokens[3][1]]))
                    elif tokens[3][1] in module.varList:
                        paramList.append((varName, module.varList[tokens[3][1]]))
                    else:
                        pass
                    #    raise VarNotDefinedError
                elif tokens[2][1] == '=':
                    expInd = 3
                    startExp = ''
                    while tokens[expInd][1] != 'to':
                        startExp += tokens[expInd][1]
                        expInd += 1
                    execute('__startpos__ = ' + startExp, module)
                    # skip 'to'
                    expInd += 1
                    endExp = ''
                    while expInd < len(tokens):
                        if tokens[expInd][1] != 'step':
                            endExp += tokens[expInd][1]
                            expInd += 1
                        else:
                            break
                    execute('__endpos__ = ' + endExp, module)
                    if expInd >= len(tokens):
                        module.varList['__step__'] = 1
                    else:
                        # skip 'step'
                        expInd += 1
                        stepExp = ''
                        while expInd < len(tokens):
                            stepExp += tokens[expInd][1]
                            expInd += 1
                        execute('__step__ = ' + stepExp, module)
                    paramList.append((varName,
                                     tuple([i for i in range(module.varList['__startpos__'],
                                                             module.varList['__endpos__'],
                                                             module.varList['__step__'])])))
                    module.varList.pop('__startpos__')
                    module.varList.pop('__endpos__')
                    module.varList.pop('__step__')
                else:
                    pass
                #    raise forStatementError
            else:
                for indx in range(len(tokens)):
                    if tokens[indx][0] in range(STATEMENTRANGE[0], STATEMENTRANGE[1]):
                        continue
                    token = token + tokens[indx][1]
                if token == '':
                    token = 'True'
                paramList.append(token)
        else:
            grammType = 'exp'
            for indx in range(len(tokens)):
                token = token + tokens[indx][1]
    return grammType, tokens, token, paramList

def runFuncs(tokens, module):
    """
    """
    newTokens = []
    for token in tokens:
        if token[0] == 2:
            funcName, paramList = getFunc(token[1])
            if funcName in module.funcList:
                func = module.funcList[funcName]
            elif funcName in module.funcList:
                func = module.funcList[funcName]
            else:
                func = None

            if func == None:
                newTokens.append(token)
            else:
                actParamValue = []
                for param in paramList:
                    if param in module.varList:
                        actParamValue.append(module.varList[param])
                    elif param in module.varList:
                        actParamValue.append(module.varList[param])
                    # else:
                    #     raise ParamUndefinedError
                module.varList.update(module.varList)
                module.funcList.update(module.funcList)
                func.passParam(actParamValue, module.varList, module.funcList)
                func.run()
                returnValue = func.get_returnVar()
                newTokens.append((3, str(returnValue)))
        else:
            newTokens.append(token)
    return tuple(newTokens)

def getFunc(token):
    funcName = ''
    paramList = []
    tmpList = token.split('(')
    funcName = tmpList[0].strip()
    paramStr = tmpList[1].strip()
    paramList = paramStr[0:len(paramStr)-1].split(',')
    for i in range(len(paramList)):
        paramList[i] = paramList[i].strip()
    return funcName, tuple(paramList)
