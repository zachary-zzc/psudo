# -*- coding: utf-8 -*-

class Node:
    __name__ = 'Node'
    __class__ = 'Node'

    def __init__(self, value=None, children=[]):
        self.value = value
        self.children = children

    def __str__(self, level=0):
        ret = '\t' * level + str(self.value) + '\n'
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    __repr__ = __str__

    def __iter__(self):
        """
        """
        for child in children:
            yield child

    def __del__(self):
        self.value = None
        self.children = []

    def __eq__(self, obj):
        return ((self.value == obj.value) and (self.children == obj.children))

    def __len__(self):
        return len(self.children)

    def __getitem__(self, ind):
        return self.children[ind]

    def __setitem__(self, ind, val):
        self.children[ind] = val

    def __delitem__(self, ind):
        return self.children.pop(ind)

    def __getslice__(self, ind1, ind2):
        return self.children[ind1:ind2]

    def __setslice__(self, ind1, ind2, val):
        self.children[ind1:ind2] = val

    def __delslice__(self, ind1, ind2):
        for ind in range(ind, ind2):
            self.children.pop(ind)

    @property
    def value(self):
        return self.value

    @property
    def children(self):
        return self.children

    @value.setter
    def value(self, value):
        self.value = value

    @children.setter
    def children(self, children):
        if (isinstance(value, list)):
            self.children = children
        else:
            raise Exception('Children should be list type')

class Tree(Node):
    def __iter__(self, tree=None, value=None, children=[]):
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
