# -*- coding: utf-8 -*-

class Node:
    __name__ = 'Node'

    def __init__(self, val=None, children=[], parent=None):
        self._val = val
        self._children = children
        self._parent = parent
        for child in self._children:
            child.parent = self

    def __str__(self):
        ret = '['
        ret += str(self.val)
        if self.hasChild:
            for child in self.children:
                if isinstance(child, Node):
                    ret += str(child)
                else:
                    ret += '[' + str(child) + ']'
        ret += ']'
        return ret

    __repr__ = __str__

    def __iter__(self):
        """
            """
        for child in self._children:
            yield child

    def __del__(self):
        self._val = None
        self._children = []

    def __eq__(self, obj):
        if isinstance(obj, Node):
            return ((self._val == obj._val) and \
                    (self._children == obj._children))
        else:
            return (self.val == obj)

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
    def val(self):
        return self._val

    @property
    def children(self):
        return self._children

    @val.setter
    def val(self, val):
        self._val = val

    @children.setter
    def children(self, children):
        if (isinstance(children, list)):
            self._children = children
        else:
            raise Exception('Children should be list type')

    @property
    def parent(self):
        return self._parent


    @parent.setter
    def parent(self, parent):
        # fix this
        self._parent = parent


    @property
    def hasParent(self):
        return (self._parent != None)


    @property
    def isRoot(self):
        return not self.hasParent


    @property
    def hasChild(self):
        return (len(self._children) != 0)

    @property
    def getHeight(self):
        if not self.hasChild:
            return 1
        childHeight = []
        for child in self._children:
            if isinstance(child, Node):
                childHeight.append(child.getHeight)
            else:
                childHeight.append(0)
        return (max(childHeight) + 1)


    def addChild(self, child):
        self._children.append(child)


