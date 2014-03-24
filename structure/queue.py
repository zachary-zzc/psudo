# -*- coding: utf-8 -*-

class Queue(list):
    __name__ = 'queue'
    __class__ = 'queue'

    @property
    def front(self):
        try:
            return self[0]
        except IndexError:
            print('Queue is Empty!')

    @property
    def back(self):
        try:
            return self[len(self)-1]
        except IndexError:
            print('Queue is Empty!')

    @property
    def isEmpty(self):
        return not self

    def enque(self, item):
        self.append(item)

    def deque(self):
        return self.pop(0)
