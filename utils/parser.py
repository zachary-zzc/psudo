# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import glb

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
        '//':           65,
        }

def preprocess(strContent):
    orig = strContent.split('\n')
    contents = []
    for line in orig:
        line = line.rstrip()
        if '#' in line:
            line = line.split('#')[0]
        if line:
            contents.append(line)
    return contents



def lexical(block):
    """
    lexical analysis:
        input: sentence, e.g., 'for i = 1 to 9, step = 10'
        output: syn, token pair (syn, token) list.
    else:
        exec(extoken, globals())

        4 kinds of syn:
        1. key words:
            for, if, else, repeat, until, while, function, is, in, or, and
        2. opts:
            +, -, *, /, <, <=, >, >=, <>, !=, =, ==, ;, (, ), &, &&, ^, %, |, ||, >>, <<, //
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
    bracket_stack = []
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
                bracket_stack.append(ch)
                if token in keywords:
                    tokens.append((keywords.get(token), token))
                    tokens.append((opts.get(ch), ch))
                    bracket_stack.pop()
                else:
                    while bracket_stack:
                        token += ch
                        indx += 1
                        if indx < len(block):
                            ch = block[indx]
                        else:
                            break
                        if ch == '(':
                            bracket_stack.append(ch)
                        elif ch == ')':
                            bracket_stack.pop()
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
            elif ch == '/':
                indx += 1
                ch = block[indx]
                if ch == '/':
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
    2. token: executable tokens for execute function use
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

    if len(tokens) != 0:
        if tokens[0][1] == 'function':
            grammType = 'defination'
            funcName, formalParamList = getFunc(tokens[1][1])
            paramList.append(funcName)
            paramList.append(formalParamList)
            token = funcName
        else:
            if tokens[0][0] == 1:
                if tokens[1][0] == 1:
                    grammType = 'defination'
                    varType = tokens[0][1]
                    varName = tokens[1][1]
                    paramList.append(varName)
                    token = varName + ' = ' + varType
                    if len(tokens) == 2:
                        token += '()'
                    else:
                        if tokens[2][1] == '=':
                            token += '('
                            for indx in range(3, len(tokens)):
                                token += tokens[indx][1] + ' '
                            token += ')'
                else:
                    grammType = 'exp'
                    for indx in range(len(tokens)):
                        token += tokens[indx][1] + ' '

            elif tokens[0][0] in range(STATEMENTRANGE[0], STATEMENTRANGE[1]):
                grammType = 'statement'

                # need to fix to generator

                if tokens[0][1] == 'for':
                    from utils.recursive import execute
                    varName = tokens[1][1]
                    if tokens[2][1] == 'in':
                        loopToken = '__loop__ = '
                        for indx in range(3, len(tokens)):
                            loopToken += tokens[indx][1]
                        execute(loopToken, module)
                        paramList.append((varName, list(eval('__loop__', module.varList))))
                        module.varList.pop('__loop__')
                    elif tokens[2][1] == '=':
                        expInd = 3
                        startExp = ''
                        while tokens[expInd][1] != 'to':
                            startExp += tokens[expInd][1] + ' '
                            expInd += 1
                        execute('__startpos__ = ' + startExp, module)
                        # skip 'to'
                        expInd += 1
                        endExp = ''
                        while expInd < len(tokens):
                            if tokens[expInd][1] != 'step':
                                endExp += tokens[expInd][1] + ' '
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
                                stepExp += tokens[expInd][1] + ' '
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

                # while and if module add statement attribution

                else:
                    for indx in range(len(tokens)):
                        if tokens[indx][0] in range(STATEMENTRANGE[0], STATEMENTRANGE[1]):
                            continue
                        token += tokens[indx][1] + ' '
                    if token == '':
                        token = 'True'
                    paramList.append(token)
            else:
                grammType = 'exp'
                for indx in range(len(tokens)):
                    token += tokens[indx][1] + ' '
    return grammType, tokens, token, paramList



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
