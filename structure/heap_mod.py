# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# -*- coding: utf-8 -*-

# <codecell>

import heapq

# <codecell>

class Heap(object):
    
    __name__='Heap'
    
    def __init__(self, items=[]):
        self._items = list(items)
        heapq.heapify(self._items)

    def __str__(self):
        return str(self._items)

    @property
    def top(self):
        return self._items[0]

    @property
    def isEmpty(self):
        return len(self) == 0


    def parent(self,i):
        return floor(i/2)


    def left(self,i):
        return (2*i)


    def right(self,i):
        return (2*i+1)   

    def pop(self):
        try:
            return heapq.heappop(self._items)
        except IndexError as e:
            raise e

    def push(self, item):
        try:
            hash(item)
        except TypeError as e:
            raise e
        else:
            heapq.heappush(self._items, item)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        while len(self) > 0:
            yield self.pop()

