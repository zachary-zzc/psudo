# -*- coding: utf-8 -*-

import utils.parser as parser
import module.commodule as commodule
import structure
import glb

def psudo(contents):
    contents = parser.preprocess(contents)
    globalModule = commodule.commodule(glb.globalVarList, glb.globalFuncList, contents)
    globalModule.run()

    hasMainFunc = 0
    for func in glb.globalFuncList:
        if func == 'Main':
            hasMainFunc = 1
            glb.globalFuncList[func].run()
    return 'success'


if __name__ == '__main__':
    fin = open('bubble.txt', "r")
    contents = fin.readlines()
    psudo("".join(contents))

