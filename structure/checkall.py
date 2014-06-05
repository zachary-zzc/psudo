import sys
sys.path.append('..')

from matrix_mod import Matrix
from graph_mod import Graph, Vertex
from digraph_mod import DiGraph
from heap_mod import Heap
from node_mod import Node

#from queue_mod import Queue
from linkedlist_mod import LinkedList
Array = list
from stack_mod import Stack
from matrix_mod import Matrix
from algorithm.random_factory import random_factory
#check_list = [Array([1, 2, 3]), Queue([1, 2, 3]), Stack(1, 2, 3)]
#check_list=[Matrix(4, 4)]
#check_list = [Array([1, 2, 3]), Stack([1, 2, 3])]
#check_list=[Vertex(1)]
#check_list=[Heap([1,2,3])]
#check_list = [random_factory(Graph)]
#check_list = [Vertex(1)]
#check_list = [Heap([1,2,3])]
#check_list= [Node(1)]


import re
from copy import deepcopy
def check():
    for item in check_list:
        print(item.__class__.__name__)
        for name in dir(item):
            attr = getattr(item, name)
            if (not hasattr(attr, '__call__')) and (not re.search(r'^_', name)):
            	tempAttr=deepcopy(attr)
            	if not isinstance(tempAttr, str) and hasattr(tempAttr,'__iter__'):
            		tempAttr = tuple(tempAttr)
            	print('{}:{}'.format(name, tempAttr))


if __name__ == '__main__':
    check()


