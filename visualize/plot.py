# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import structure
import glb
import pydot
import time
import functools

SINGLETYPE = (str,
              int,
              )
ARRAYTYPE = (list,
             tuple,
             dict,
             set, )
TREETYPE = ()
GRAPHTYPE = ()
DIGRAPHTYPE = ()

def plot():
    path = r'test.png'
    graph = pydot.Dot(graph_type='graph')
    for i in range(len(glb.moduleStack)):
        subGraph = pydot.Cluster()
        if i == 0:
            subGraph.set_name == 'global'
        elif(type(glb.moduleStack[i]) == 'funcmodule.funcmodule'):
            subGraph.set_name == glb.moduleStack[i].get_FuncName()
        for varName in glb.moduleStack[i].localVarList:
            var = eval(varName, glb.moduleStack[i].varList)
            if isinstance(var, SINGLETYPE):
                graph_type = 'single'
            elif isinstance(var, ARRAYTYPE):
                graph_type = 'array'
            elif isinstance(var, TREETYPE):
                graph_type = 'tree'
            elif isinstance(var, GRAPHTYPE):
                graph_type = 'graph'
            elif isinstance(var, DIGRAPHTYPE):
                graph_type = 'digraph'
            varGraph = plot_var(varName, var, graph_type)
            subGraph.add_subgraph(varGraph)
        graph.add_subgraph(subGraph)
    graph.write_png(path)
    # show(path)

def plot_var(varName, var, graph_type):
    varGraph = pydot.Cluster(graph_name=varName)
    if graph_type == 'single':
        node = pydot.Node(str(var))
        varGraph.add_node(node)
    elif graph_type == 'array':
        # edge or node
        # edge
        # for i in range(len(var) - 1):
        #     edge = pydot.Edge(str(var[i]), str(var[i+1]))
        #     varGraph.add_edge(edge)
        # node
        for i in range(len(var)):
            node = pydot.Node(str(var[i]))
            varGraph.add_node(node)
    elif graph_type == 'tree':
        pass
    elif graph_type == 'graph':
        pass
    elif graph_type == 'digraph':
        pass
    return varGraph

def refresh(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        for module in glb.moduleStack:
            for key in module.localVarList:
                outputVar = '{}: {}'.format(key, module.varList[key])
                print(outputVar)
        plot()
        #time.sleep(0.5)
        input()
        return ret
    return wrapper
