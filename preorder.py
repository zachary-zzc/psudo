from structure.config import *

def pre(tree):
    if tree != None:
        print(tree.value)
        pre(tree.left)
        pre(tree.right)

a = Node('a')
b = Node('b')
c = Node('c', [a, b])
btree = BTree('root', c)

if __name__ == '__main__':
    pre(btree)
