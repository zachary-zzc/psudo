# -*-coding: utf-8 -*-

class Stack(list):
    __name__ = 'Stack'

    @property
    def top(self):
        if self:
            return self[len(self)-1]
        else:
            return None

    @property
    def isEmpty(self):
        return not self

    def push(self, item):
        self.append(item)
