# -*- coding: utf-8 -*-

class Node:
    __name__ = 'Node'
    __class__ = 'Node'

    def __init__(self, value=None, children=[]):
        self._val = value
        self._children = children

    def __str__(self, level=0):
        ret = '\t' * level + str(self._val) + '\n'
        for child in self._children:
            if isinstance(child, Node):
                ret += child.__str__(level+1)
            else:
                ret += '\t' * (level+1) + str(child) + '\n'
        return ret

    __repr__ = __str__

    def __iter__(self):
        """
        """
        for child in children:
            yield child

    def __del__(self):
        self._val = None
        self._children = []

    def __eq__(self, obj):
        return ((self._val == obj.value) and (self._children == obj.children))

    def __len__(self):
        return len(self._children)

    def __getitem__(self, ind):
        return self._children[ind]

    def __setitem__(self, ind, val):
        self._children[ind] = val

    def __delitem__(self, ind):
        return self._children.pop(ind)

    def __getslice__(self, ind1, ind2):
        return self._children[ind1:ind2]

    def __setslice__(self, ind1, ind2, val):
        self._children[ind1:ind2] = val

    def __delslice__(self, ind1, ind2):
        for ind in range(ind, ind2):
            self._children.pop(ind)

    @property
    def value(self):
        return self._val

    @property
    def children(self):
        return self._children

    @value.setter
    def value(self, value):
        self._val = value

    @children.setter
    def children(self, children):
        if (isinstance(children, list)):
            self._children = children
        else:
            raise Exception('Children should be list type')

    def append(self, child):
        self._children.append(child)

class Tree(Node):
    def __init__(self, tree=None, value=None, children=[]):
        if tree is not None:
            if (isinstance(tree, Tree)):
                self = tree
            else:
                raise Exception('tree should be Tree type')
        else:
            self.root = Node(value, children)

    def preorder_traversal(self, func):
        pass

    def inorder_traversal(self, func):
        pass

    def postorder_traversal(self, func):
        pass
