# -*-coding: utf-8 -*-

from queue import Queue as TemplateQueue

class Queue(TemplateQueue):
    """Self-defined Queue"""

    __name__="Queue"

    @property
    def isEmpty(self):
        return self.empty()

    def enqueue(self,item):
        self._put(item)

    def dequeue(self):
        return self._get()
