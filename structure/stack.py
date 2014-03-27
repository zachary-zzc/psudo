# -*-coding: utf-8 -*-

class Stack(list):
    __name__ = 'Stack'
    __class__ = 'Stack'

    @property
    def top(self):
        return self[len(self)-1]

    @property
    def isEmpty(self):
        return not self

    def push(self, item):
        self.append(item)
