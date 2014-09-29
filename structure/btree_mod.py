# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from structure.tree_mod import Tree, Node

def node2btree(node):
    btree = BTree(node.val)
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
    def __init__(self, val=None, left=None, right=None, parent=None):
        self._val = val
        self._children = [left, right]
        self._parent = parent
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
    def left(self, val):
        self._children[0] = val

    @property
    def hasLeft(self):
        return (self.left != None)

    @property
    def right(self):
        return self._children[1]

    @right.setter
    def right(self, val):
        self._children[1] = val

    @property
    def hasRight(self):
        return (self.right != None)

    def insert(self, node):
        node = node2btree(node)
        y = None
        x = self
        while (x != None) and (x.val != None):
            y = x
            if node.val < x.val:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y == None:
            self = node
        elif node.val < y.val:
            y.left = node
        else:
            y.right = node
        return self

    def delete():
        pass

    def search():
        pass

