# -*- coding: utf-8 -*-
import random
import string
import sys
sys.path.append('..')

from structure.config import *

List_type = [Array, list, Stack]  #Queue

def random_factory(cls):

    if cls is Graph:
        
        vertex=[]           #init list of vertex
        edge=[]             #init list of edge
        edge_inverse=[]     #init list for inverse edge

        num_vertex=random.randrange(5,10)                                       #randomize the number of vertex
        num_edge=random.randrange(0,num_vertex*(num_vertex-1)/2-num_vertex+1)     #randomize the number of edge

        for x in range(0,num_vertex):           #denominate the vertexex
            temp=id_generator()
            while temp in vertex:
                temp=id_generator()
            vertex.append(temp)

        for i in range(0,num_vertex-1,1):
            edge.append([vertex[i],vertex[i+1]])

        for y in range(0,num_edge):             #denominate the edges based on the vertexex above
            temp=[id_generator(1,vertex),id_generator(1,vertex)]
            temp_inverse=[temp[1],temp[0]]
            while temp in edge_inverse or temp_inverse in edge_inverse or (temp==temp_inverse):         #remove the inverse edge
                temp=[id_generator(1,vertex),id_generator(1,vertex)]
                temp_inverse=[temp[1],temp[0]]
            edge.append(temp)
            edge_inverse.append(temp)
            edge_inverse.append(temp_inverse)

        return Graph(vertex,edge)

    elif cls is DiGraph:

        vertex=[]       #init list of vertex
        edge=[]         #init list of edge

        num_vertex=random.randrange(5,10)                                       #randomize the number of vertex
        num_edge=random.randrange(0,num_vertex*(num_vertex-1)+1)                #randomize the number of edge

        for x in range(0,num_vertex):               #denominate the vertexex
            temp=id_generator()
            while temp in vertex:
                temp=id_generator()
            vertex.append(temp)

        for i in range(0,num_vertex-1,1):
            edge.append([vertex[i],vertex[i+1]])

        for y in range(0,num_edge):                 #denominate the edges based on the vertexex above
            temp=[id_generator(1,vertex),id_generator(1,vertex)]
            while temp in edge:
                temp=[id_generator(1,vertex),id_generator(1,vertex)]
            edge.append(temp)

        return  DiGraph(vertex,edge)


    elif cls in List_type:
        temp=[int(id_generator(chars=string.digits)) for i in range(int(id_generator(chars=string.digits)))]
        # if cls is LinkedList:
        #     ret = LinkedList()
        #     map(ret.insert, ret)
        #     return ret
        # else:
        return cls(temp)

    elif cls is BinaryTree:
        temp = BinaryTree()
        num_node=random.randrange(5,10)
        for i in range(num_node):
            tmpvalue=int(id_generator(1,string.digits))
            temp.insert(tmpvalue,tmpvalue)
        return temp
    elif cls is AVLTree:
        temp=AVLTree()
        num_node=random.randrange(5,10)
        for i in range(num_node):
            tmpvalue=int(id_generator(1,string.digits))
            temp.insert(tmpvalue,tmpvalue)
        return temp
    elif cls is RBTree:
        temp=RBTree()
        num_node=random.randrange(5,10)
        for i in range(num_node):
            tmpvalue=int(id_generator(1,string.digits))
            temp.insert(tmpvalue,tmpvalue)
        return temp
    elif cls is LinkedList:
        linkedlist=LinkedList()
        temp=[int(id_generator(chars=string.digits)) for i in range(int(id_generator(chars=string.digits)))]
        for item in temp:
            linkedlist.insert(item)
        return linkedlist
    elif cls is Heap:
        heap=Heap()
        temp=[int(id_generator(chars=string.digits)) for i in range(int(id_generator(chars=string.digits)))]
        for item in temp:
            heap.push(item)
        return heap
    else:
        pass


def id_generator(size=1, chars=string.ascii_uppercase):                 #+string.digits
    return ''.join(random.choice(chars) for _ in range(size))
