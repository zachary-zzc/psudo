# -*- coding: utf-8 -*-

import utils
import module
import structure

def psudo(context):
    globalVarList, mainContext = preprocess(context)

    if len(mainContext) != 0:
        mainFunc = module.main(context = mainContext, varList = globalVarList)
    else:
        mainFunc = module.main(context = context)

    mainFunc.run()
