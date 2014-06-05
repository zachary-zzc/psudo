# -*-coding: utf-8 -*-

import sys
sys.path.append('..')


class Node():
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

    def __str__(self):
        return 'value: {}'.format(self.value)


    __repr__ = __str__




class LinkedList(list):

    __name__ = "LinkedList"

    def __init__(self):
        pass


    def __str__(self):
        return str([node.value for node in self])

    @property
    def length(self):
        return len(self)


    @property
    def head(self):
        if self:
            return self[0]
        else:
            return None


    @staticmethod
    def _get_index(list_obj, condition):
        return list(map(condition, list_obj)).index(True)


    def search(self, key):
        if self.head == None:
            return None
        else:
            indx = LinkedList._get_index(self, lambda x: x.value == key)
            if indx >= 0:
                return self[indx]
            else:
                return None


    def insert(self, node):
        if self.head == None:
            self.append(Node(node, None, None))
        else:
            new_node = Node(node, self[self.length-1], None)
            self[self.length-1].next = new_node
            self.append(new_node)


    def delete(self,node):
        if self.length != 0:
            indx = LinkedList._get_index(self, lambda x: x.value == node)
            if indx == self.length-1 and indx == 0:
                pass
            elif indx == self.length-1:
                self[indx-1].next = None
            elif indx == 0:
                self[indx+1].prev = None
            else:
                self[indx-1].next = self[indx+1]
                self[indx+1].prev = self[indx-1]
            self.pop(indx)
        else:
            raise IndexError('Linked List is Empty')
