from matrix import Matrix
from graph import Graph
from digraph import DiGraph

from queue import Queue
from linkedlist import LinkedList
Array = list
from stack import Stack
from matrix import Matrix

# check_list = [Array([1, 2, 3]), Queue([1, 2, 3]), Stack(1, 2, 3)]
check_list = [Array([1, 2, 3]), Stack([1, 2, 3]), Matrix([1, 2, 3])]


import re
def check():
    for item in check_list:
        print(item.__class__.__name__)
        for name in dir(item):
            attr = getattr(item, name)
            if (not hasattr(attr, '__call__')) and (not re.search(r'^_', name)):
                print('{}:{}'.format(name, attr))


if __name__ == '__main__':
    check()


