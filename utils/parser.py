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
    # as python, '#' stands for annotation
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



# check to remove module input, as the output of parser should only be determined by
# input sentence and grammer

def parse(block, module):
    """
    Input: sentence, same with lexical
           funcList, for convinient use, should not appear here
    Output:
    1. gramm_type: 'defination', 'statement', 'exp'
    2. token: executable tokens for execute function use
    3. param_list: Due to gramm_type.
        If block is var defination, param_list[0] = var_name
        If block is function defination, param_list[0] = func_name
                                         param_list[1] = formal_param_list
        if block is if or while statement, param_list[0] is there judge exp
        if block is for statement, param_list[0] is iter var_name and iter list
                                   e.g 'for i = 1 to 10, step 1'
                                   param_list[0] = ('i', (1, 2, 3, ..., 10))

    for statement have two types:
        1. for [var_name] in [iterableList]
        2. for [var_name] = [startpos] to [endpos] step [step]
    """

    gramm_type = ''
    token = ''
    param_list = []
    tokens = lexical(block)

    if len(tokens) != 0:
        if tokens[0][1] == 'function':
            gramm_type = 'defination'
            func_name, formal_param_list = get_func_info(tokens[1][1])
            param_list.append(func_name)
            param_list.append(formal_param_list)
            token = func_name
        else:
            if tokens[0][0] == 1:
                if tokens[1][0] == 1:
                    gramm_type = 'defination'
                    var_type = tokens[0][1]
                    var_name = tokens[1][1]
                    param_list.append(var_name)
                    token = var_name + ' = ' + var_type
                    if len(tokens) == 2:
                        token += '()'
                    else:
                        if tokens[2][1] == '=':
                            token += '('
                            for indx in range(3, len(tokens)):
                                token += tokens[indx][1] + ' '
                            token += ')'
                else:
                    gramm_type = 'exp'
                    for indx in range(len(tokens)):
                        token += tokens[indx][1] + ' '

            elif tokens[0][0] in range(STATEMENTRANGE[0], STATEMENTRANGE[1]):
                gramm_type = 'statement'

                # need to fix to generator

                if tokens[0][1] == 'for':
                    from utils.recursive import execute
                    var_name = tokens[1][1]
                    if tokens[2][1] == 'in':
                        loopToken = '__loop__ = '
                        for indx in range(3, len(tokens)):
                            loopToken += tokens[indx][1]
                        execute(loopToken, module)
                        param_list.append((var_name, list(eval('__loop__', module.var_list))))
                        module.var_list.pop('__loop__')
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
                            module.var_list['__step__'] = 1
                        else:
                            # skip 'step'
                            expInd += 1
                            stepExp = ''
                            while expInd < len(tokens):
                                stepExp += tokens[expInd][1] + ' '
                                expInd += 1
                            execute('__step__ = ' + stepExp, module)
                        param_list.append((var_name,
                                         tuple([i for i in range(module.var_list['__startpos__'],
                                                                 module.var_list['__endpos__'],
                                                                 module.var_list['__step__'])])))
                        module.var_list.pop('__startpos__')
                        module.var_list.pop('__endpos__')
                        module.var_list.pop('__step__')
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
                    param_list.append(token)
            else:
                gramm_type = 'exp'
                for indx in range(len(tokens)):
                    token += tokens[indx][1] + ' '
    return gramm_type, tokens, token, param_list



def get_func_info(token):
    func_name = ''
    param_list = []
    tmpList = token.split('(')
    func_name = tmpList[0].strip()
    paramStr = tmpList[1].strip()
    param_list = paramStr[0:len(paramStr)-1].split(',')
    for i in range(len(param_list)):
        param_list[i] = param_list[i].strip()
    return func_name, tuple(param_list)
