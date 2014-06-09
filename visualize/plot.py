# -*- coding: utf-8 -*-

import sys
import re
sys.path.append('..')

from module.funcmodule import funcmodule

from copy import deepcopy

from structure.config import *
import glb
import time
import functools

from xml.dom import minidom, Node

def record_to_xml():

    doc = minidom.Document()
    params = doc.createElement('Params')
    doc.appendChild(params)

    for module in glb.module_stack:
        for varName in module.local_var_list:
            var = eval(varName, glb.global_var_list, module.var_list)
            xmlVar = doc.createElement('var')
            xmlVar.setAttribute('name', varName)
            xmlVar.setAttribute('type', var.__class__.__name__)
            xmlVarValue = doc.createElement('value')
            xmlVarValue.appendChild(doc.createTextNode(str(var)))
            xmlVar.appendChild(xmlVarValue)
            params.appendChild(xmlVar)


            for name in dir(var):
                attr=getattr(var,name)
                if(not hasattr(attr,'__call__')) and (not re.search(r'^_',name)):
                    xmlAttr=doc.createElement('attr')
                    xmlAttr.setAttribute('name',name)
                    xmlAttrValue = doc.createElement('value')
                    xmlAttrValue.appendChild(doc.createTextNode(str(attr)))
                    xmlAttr.appendChild(xmlAttrValue)
                    if not isinstance(attr, str) and hasattr(attr, '__iter__'):
                        for index, item in enumerate(attr):
                            add_xml_attr(doc, index, item, xmlAttr)
                    xmlVar.appendChild(xmlAttr)

    with open(r'visualize/release1.1/varList.xml', 'w') as f:
        f.write(doc.toprettyxml(indent = ''))


def add_xml_attr(doc, index, item, xmlAttr):
    xmlVar = doc.createElement(item.__class__.__name__)
    xmlVar.setAttribute('index',str(index))
    for name in dir(item):
        attr = getattr(item, name)
        if not hasattr(attr, '__call__') and not re.search(r'^_', name):
            xmlVar.setAttribute(name, str(attr))
    xmlVar.appendChild(doc.createTextNode(str(item)))
    # add_xml_attr(doc, item, xmlVar)
    xmlAttr.appendChild(xmlVar)



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
