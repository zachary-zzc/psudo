#-*- coding: utf-8 -*-
import sys
sys.path.append('..')

from module.ifelsemodule import ifelsemodule
from module.formodule import formodule
from module.whilemodule import whilemodule
from module.funcmodule import funcmodule

from structure.config import *

import utils.parser as parser
import visualize.plot as plot
import glb

# module type
function_module = (funcmodule, )
loop_module = (whilemodule, formodule, )
branch_module = (ifelsemodule, )

def recursive(content, index, module):
    """
    recursively execute sentences

    Grammer structure:
    Defination: Define variables or functions, because the character of psudocode,
                assignment statement are also considered as defination

    Expression: Operations

    Statement: Including if, while, for and repeat/until, break, continue, return.
    """
    if module.end_recursive:
        return
    else:
        if (index < len(content)) and (content[index]):
            print('compile content : {}'.format(content[index]))
            # preprocess should remove all annotations and useless whitespaces as well as blank lines
            gramm_type, tokens, extoken, param_list = parser.parse(content[index], module)
            #----------DEFINATION---------
            if gramm_type == 'defination':
                if tokens[0][1] == 'function':
                    count = get_module_index(content, index)
                    module_content = [content[index+i] for i in range(1, count)]
                    func_name = param_list[0]
                    param_list = param_list[1]
                    funcModule = funcmodule(func_name, param_list, module_content)
                    module._func_inc(func_name, funcModule)
                    index += count
                else:
                    var_name = param_list[0]
                    module._var_inc(var_name, 0)
                    execute(extoken, module)
                    index += 1
            #---------EXPRESSION----------
            elif gramm_type == 'exp':
                execute(extoken, module)
                index += 1
                #---------STATEMENT----------
            elif gramm_type == 'statement':

                # continue, break, and return
                # haven't tested yet, waiting for debug

                # deal with "return" statement:
                #    reverse stop modules in module_stack until meet last function module
                if tokens[0][1] == 'return':
                    try:
                        # test return multiple values
                        module.return_list = eval(extoken, glb.global_var_list, module.var_list)
                    except AttributeError:
                        print('SyntaxError: return statement should be in a function')
                        sys.exit(1)
                    for module in reversed(glb.module_stack):
                        if not isinstance(module, function_module):
                            module.setEnd()
                        else:
                            break
                    return

                # deal with "break" and "continue "statement:
                #   similiar with "return" statement
                if (tokens[0][1] == 'break') or (tokens[0][1] == 'continue'):
                    for module in reversed(glb.module_stack):
                        if not isinstance(module, loop_module):
                            module.setEnd()
                        else:
                            # first "not loop" module
                            module.setEnd()
                            if tokens[0][1] == 'continue':
                                module.setContinue()
                            break
                    return

                # if, while, and for
                count = get_module_index(content, index)
                module_content = [content[index+i] for i in range(1, count)]
                exp = param_list[0]

                if tokens[0][1] == 'if':
                    exps = [exp]
                    contents = [module_content]
                    index += count

                    # find better way to write this part, a little bit ugly
                    if index < len(content):
                        gramm_type, tokens, extoken, param_list = parser.parse(content[index],
                                module)
                        while tokens[0][1] == 'else':
                            count = get_module_index(content, index)
                            contents.append([content[index+i] for i in range(1, count)])
                            index += count
                            exp = param_list[0]
                            exps.append(exp)
                            if index >= len(content):
                                break
                            gramm_type, tokens, extoken, param_list = parser.parse(content[index],
                                    module)

                    ifModule = ifelsemodule(module.var_list,
                                            module.func_list,
                                            exps,
                                            contents)
                    ifModule.run()
                    index -= count

                elif tokens[0][1] == 'for':
                    forModule = formodule(module.var_list,
                                          module.func_list,
                                          exp,
                                          module_content)
                    forModule.run()

                elif tokens[0][1] == 'while':
                    whileModule = whilemodule(module.var_list,
                                              module.func_list,
                                              exp,
                                              module_content)
                    whileModule.run()
                # elif tokens[0][1] == 'repeat':
                #     pass

                index += count

            recursive(content, index, module)



def get_module_index(content, index):
    """
    """
    count = 1
    while index+count < len(content):
        indxInd = len(content[index]) - len(content[index].lstrip())
        countInd = len(content[index+count]) - len(content[index+count].lstrip())
        if countInd > indxInd:
            count += 1
        else:
            break
    return count



@plot.refresh
def execute(extoken, module):
    print('exec token : {}'.format(extoken))

    # stupid here...
    var_list_bak = {}
    var_list_bak.update(module.var_list)
    try:
        exec(extoken, glb.global_var_list, module.var_list)
    except Exception:
        raise

    for key in module.var_list.keys():
        if (key not in var_list_bak) and (key.find('__') != 0):
            module.local_var_list.append(key)
