# -*- coding: utf-8 -*-
import random
import string
import btree from structure

def random(class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        ):

    if ClassName=="Graph":
        
        vertex=[]           #init list of vertex
        edge=[]             #init list of edge
        edge_inverse=[]     #init list for inverse edge

        num_vertex=random.randrange(5,10)                                       #randomize the number of vertex
        num_edge=random.randrange(0,num_vertex*(num_vertex-1)/2+num_vertex)     #randomize the number of edge

        for x in range(0,num_vertex):           #denominate the vertexex
            temp=id_generator()
            while temp in vertex:
                temp=id_generator()
            vertex.append(temp)

        for y in range(0,num_edge):             #denominate the edges based on the vertexex above
            e=id_generator(2,vertex)
            temp='('+e[0]+','+e[1]+')'
            temp_inverse = '('+e[1]+','+e[0]+')'
            while temp in edge_inverse or temp_inverse in edge_inverse:         #remove the inverse edge
                e=id_generator(2,vertex)
                temp='('+e[0]+','+e[1]+')'
                temp_inverse = '('+e[1]+','+e[0]+')'
            edge.append(temp)
            edge_inverse.append(temp)
            edge_inverse.append(temp_inverse)

        return Graph(vertex,edge)


    elif ClassName=="DiGraph":

        vertex=[]       #init list of vertex
        edge=[]         #init list of edge

        num_vertex=random.randrange(5,10)                                       #randomize the number of vertex
        num_edge=random.randrange(0,num_vertex*(num_vertex-1)+num_vertex)       #randomize the number of edge

        for x in range(0,num_vertex):               #denominate the vertexex
            temp=id_generator()
            while temp in vertex:
                temp=id_generator()
            vertex.append(temp)

        for y in range(0,num_edge):                 #denominate the edges based on the vertexex above
            e=id_generator(2,vertex)
            temp='('+e[0]+','+e[1]+')'
            while temp in edge:
                e=id_generator(2,vertex)
                temp='('+e[0]+','+e[1]+')'
            edge.append(temp)

        return  DiGraph(vertex,edge)


    elif ClassName=="BTree":

        num_node=random.randrange(8,15)             
        btree=None

        for z in range(0,num_node):

            node = BTree(int(id_generator(1,string.digits)))
            btree = TREE_INSERT(btree, node)

    else:
        pass



def id_generator(size=1, chars=string.ascii_uppercase):                 #+string.digits
    return ''.join(random.choice(chars) for _ in range(size))