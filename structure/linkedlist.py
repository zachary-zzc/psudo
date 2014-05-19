# -*-coding: utf-8 -*-

import sys
sys.path.append('..')

from structure.node import Node

class LinkedList(Node):

    __name__="LinkedList"

    def __init__(self):
        self._length = 0
        self._head   = None

    @property
    def head(self):
        return self._head

def list_search(self,key):
    node=self._head
    while node != None and node._value != key:
        node=node._children[0]
    return node

def list_insert(self,node):
    node._children[0]=self._head
    if self._head != None:
        self._head._parent=node
    self._head = node
    node._parent = None
    self._length += 1

def list_delete(self,node):
    if self._length != 0:
        if not node.isRoot:
            node._parent._children[0] = node._children[0]
        else:
            self._head = node._children[0]
        if node.hasChild:
            node._children[0]._parent=node._parent
        self._length -= 1;
    else:
        print("The linked list is Empty!")
