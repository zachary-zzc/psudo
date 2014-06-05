# import sys
# sys.path.append('..')


from bintrees.bintree import BinaryTree
from bintrees.avltree import AVLTree
from bintrees.rbtree import RBTree



def check():
    #A = BinaryTree()
    A = AVLTree()
    #A = RBTree()
    A.insert(5,"5")
    A.insert(6,"6")
    A.insert(16,"16")
    A.insert(2,"2")
    A.insert(25,"25")
    A.insert(14,"14")
    print(A)

if __name__ == '__main__':
    check()