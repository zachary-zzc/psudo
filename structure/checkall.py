import sys
sys.path.append('..')

from config import *
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
check_list=[random_factory(LinkedList)]


import re
from copy import deepcopy
def check():

    #print(type(check_list[0].V[0]))
    #print(check_list[0].top)
    for item in check_list:
        print(item.__class__.__name__)
        print('value: {}'.format(str(item)))
        for name in dir(item):
            attr = getattr(item, name)
            if (not hasattr(attr, '__call__')) and (not re.search(r'^_', name)):
            	tempAttr=deepcopy(attr)
            	if not isinstance(tempAttr, str) and hasattr(tempAttr,'__iter__'):
            		tempAttr = tuple(tempAttr)
            	print('Attr name: {}, Attr value: {}'.format(name, tempAttr))
def check2():
    for item in check_list:
        print(item.__class__.__name__)
        print('value: {}'.format(str(item)))
        for name in dir(item):
            attr = getattr(item, name)
            if (not hasattr(attr, '__call__')) and (not re.search(r'^_', name)):
                if not isinstance(attr, str) and hasattr(attr,'__iter__'):

                    print('Attr name: {}, Attr value: {}'.format(name, attr))

if __name__ == '__main__':
    check()


