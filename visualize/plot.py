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


def trans_vex(vex):
    return {'value': vex.value,
            'color': vex.color,
            'adjs': vex.adjs}

def trans_edge(edge):
    return {'start': edge.start,
            'end': edge.end,
            'weight': edge.weight}


import json

SPEC_TYPES=(str, Vertex, Edge)

def status_dict():
    ret = {}
    ret['current_line'] = glb.current_line
    ret['current_content'] = glb.current_content
    # ret['msg'] =
    ret['vars'] = []

    for module in glb.module_stack:
        for varName in module.local_var_list:
            var = eval(varName, glb.global_var_list, module.var_list)
            newItem = {}
            newItem['name'] = varName
            newItem['type'] = var.__class__.__name__
            newItem['value'] = str(var)
            for attrName in dir(var):
                attr = getattr(var, attrName)
                if (not hasattr(attr, '__call__')) and (not re.search(r'^_', attrName)):
                    if not isinstance(attr, SPEC_TYPES) and hasattr(attr, '__iter__'):
                        newItem[attrName] = list_scanner(attr)
                    elif isinstance(attr, Vertex):
                        newItem[attrName] = trans_vex(attr)
                    elif isinstance(attr, Edge):
                        newItem[attrName] = trans_edge(attr)
                    else:
                        newItem[attrName] = attr
            ret['vars'].append(newItem)
    return ret



def list_scanner(l):
    ret = []
    for item in l:
        if not isinstance(item, SPEC_TYPES) and hasattr(item, '__iter__'):
            ret.append(list_scanner(item))
        else:
            if isinstance(item, Vertex):
                ret.append(trans_vex(item))
            elif isinstance(item, Edge):
                ret.append(trans_edge(item))
            else:
                ret.append(item)
    return ret







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
        # record_to_xml()
        glb.var_dict['statement_{}'.format(glb.step)] = status_dict()
        glb.step += 1
        with open(r'visualize/release1.1/varList.json', 'w') as f:
            json.dump(glb.var_dict, f, sort_keys=True, indent=4)
        # time.sleep(0.1)
        # input()
        return module
    return wrapper
