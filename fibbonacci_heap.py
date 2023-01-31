# Created By Team 6: Bryson Duckworth, Alyssa Gabrielson, Will Miller, Riley Parker, Sydney Pierce, Luke Roberts, & Joey Walker

class Node:
    def __init__(self):
        self.key = -1       # key value
        self.parent = None  # pointer to parent
        self.child = None   # pointer to a child
        self.left = None    # pointer to left sibling
        self.right = None   # pointer to right sibling
        self.degree = -1    # number of children
        self.mark = False   # mark if child has been removed since insertion
    
class FibonacciHeap:
    def __init__(self):
        self.min = Node()   # pointer to minimum key node
        self.numNodes = 0   # stores total number of nodes
        self.hashTable = {} # dictionary for O(1) search
        self.numTrees = 0
#First attempt at consolidate. 
#1. Checks the roots in the list to see if two roots have the same degree.
#2. Merges the two trees into one root by using the  as the root with the smaller key. The larger key root
#becomes the child.
#3 This process is repeated until all roots in the list have different degrees.
    def __consolidate(self):
        A = [None] * self.numNodes
        root = self.min
        counter = self.numTrees
        while counter:
            x = root
            root = root.right
            d = x.degree
            while A[d]:
                y = A[d]
                if x.key > y.key:
                    x,y = y,x
                self.link(y,x)
                A[d] = None
                d += 1
            A[d] = x
            counter -= 1
        self.min = None
        for i in range(len(A)):
            if A[i]:
                if self.min == None:
                    self.min = A[i]
                else:
                    if A[i].key < self.min.key:
                        self.min = A[i]

    #Makes y the child of x. The number of marks of the node also gets updated.
    def link(self, y, x):
        self.removeRoot(y)
        if y.mark == True:
            self.numMarks -= 1
        x.add_child(y)


    #Remove the root from the list of roots in the heap.
    #This will update the pointers of the remaining roots
    #as well as the number of trees in the root list.
    def remove_root(self,x):
        right_of_x, left_of_x = x.right, x.left
        right_of_x.left = left_of_x
        left_of_x.right = right_of_x
        self.numTrees -= 1

    # Cut the node from the tree and place in the root list
    def __cut(self, node, parent):

        # Cut from child list of parent
        if node == node.left and node == node.right:
            parent.child = None
        else:
            if node == node.right:
                parent.child = node.left
                node.left.right = None
            elif node == node.left:
                parent.child = node.right
                node.right.left = None
            else:
                parent.child = node.left
                node.left.right = node.right
                node.right.left = node.left                
        parent.degree =- 1

        # Place in the root list
        self.min.left.right = node
        node.right = self.min
        node.left = self.min.left
        self.min.left = node
        node.parent = None
        node.mark = False
    
    # Cut all parent/grandparent nodes that are marked
    def __cascadeCut(self, node):
        parent = node.parent
        if parent != None:
            if parent.mark == False:
                parent.mark = True
            else:
                self.__cut(node, parent)
                self.__cascadeCut(parent)
    
    # Returns the node with the specified key
    def search(self, key):
        return self.hashTable[key]
    
    # Method that inserts a new node into the FibonacciHeap
    def insert(self, node):
        new_node = Node()
        new_node.key = node
        new_node.left = new_node
        new_node.right = new_node
        if self.numNodes == 0:
            self.min = new_node
        else:
            self.min.left.right = new_node
            new_node.right = self.min
            new_node.left = self.min.left
            self.min.left = new_node
            if new_node.key < self.min.key:
                self.min = new_node
        self.hashTable[new_node.key] = new_node
        self.numNodes += 1
    
    # Remove the node from the fibonacci heap
    def delete(self, node):
        self.decreaseKey(node, 0)
        self.extractMin()
    
    # Return the node with the minimum key
    def findMin(self):
        return self.min
    
    # Remove and return minimum node from the fibonacci heap
    def extractMin(self):

        if self.numNodes == 0:
            print("No nodes to remove")
        else:
            # Find new min
            # Set new min
            # Remove old min
            # Consolidate tree
            print("TODO")
        
        
        self.hashTable.pop(self.min.key)
        self.numNodes -= 1
    
    # Concat one tree to another
    # To Do add better comments
    def union(self, other):
        
        if self.numNodes == 0:
            self.min = other.min
        elif other.numNodes != 0:
            self.min.left.right = other.min
            other.min.left.right = self.min
            temp = self.min.left
            self.min.left = other.min.left
            other.min.left = temp
        
        if self.min.key > other.min.key:
            self.min = other.min
    
    # Decrease the key value of the given node
    def decreaseKey(self, node, newKey):
        self.hashTable[newKey] = node
        self.hashTable.pop(node.key)
        
        node.key = newKey
        temp = node.parent

        # if not in root list
        if temp != None:
            # if new key is less than parent key
            if node.key < temp.key:
                self.__cut(node, temp)
                self.__cascadeCut(temp)
        
        # if new key is less than current minimum key, replace
        if (node.key < self.min.key):
            self.min = node