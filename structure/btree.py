# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from structure.tree import Tree, Node

def node2btree(node):
    btree = BTree(node.value)
    if len(node.children) > 2:
        raise Exception('Cannot convert to BTree from a node have more than 2 children!')
    if len(node.children) == 1:
        btree.left = node2btree(node.children[0])
    elif len(node.children) == 2:
        btree.left = node2btree(node.children[0])
        btree.right = node2btree(node.children[1])
    return btree

class BTree(Tree):
    __name__ = 'BTree'
    __class__ = 'BTree'
    def __init__(self, value='default', left=None, right=None):
        self._value = value
        self._children = [left, right]
        if self.hasLeft:
            self.left = node2btree(self.left)
        if self.hasRight:
            self.right = node2btree(self.right)

    @property
    def hasChild(self):
        return (self.hasLeft or self.hasRight)

    @property
    def left(self):
        return self._children[0]

    @left.setter
    def left(self, value):
        self._children[0] = value

    @property
    def hasLeft(self):
        return (self.left != None)

    @property
    def right(self):
        return self._children[1]

    @right.setter
    def right(self, value):
        self._children[1] = value

    @property
    def hasRight(self):
        return (self.right != None)
