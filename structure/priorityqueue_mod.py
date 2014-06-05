# -*-coding: utf-8 -*-

from queue_mod import Queue

class PriorityQueue(Queue)
	
	__name__="PriorityQueue"

	def _init(self, maxsize):
		self.queue = []

	def size(self):
		return len(self.queue)

	def enqueue(self, item):
		heappush(self.queue, item)

	def dequeue(self):
		return heappop(self.queue)