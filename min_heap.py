# Course: CS261 - Data Structures
# Assignment: 5
# Student: Brian Rud
# Description: An implementation of the min heap ADT.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *

class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass

class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        Adds a new object to the MinHeap maintaining the heap property
        """
        insert_index = self.heap.length()

        if insert_index == 0:
            self.heap.append(node)
            return
        
        parent_index = (insert_index - 1) // 2

        insert_node = node
        parent_node = self.heap.get_at_index(parent_index)

        self.heap.append(node)

        while(insert_node < parent_node and parent_index >= 0):
            # swap values at parent index and insert index
            temp = insert_node
            self.heap.set_at_index(insert_index, parent_node)
            self.heap.set_at_index(parent_index, temp)

            # update insert and parent indices
            insert_index = parent_index
            parent_index = (parent_index - 1) // 2

            if insert_index == 0:
                break

            # update insert and parent values
            insert_node = self.heap.get_at_index(insert_index)
            parent_node = self.heap.get_at_index(parent_index)

    def get_min(self) -> object:
        """
        Returns an object with a minimum key without removiing it from the heap.  If the heap is
        empty, the a MinHeapException is raised
        """
        try:
            return self.heap.get_at_index(0)

        except IndexError:
            raise MinHeapException

    def remove_min(self) -> object:
        """
        Returns an object with a minimum key and removes it from the heap.  If the heap is empty, the
        method raises a MinHeapException
        """
        # get the value to return - if the min_heap is empty, this will raise a MinHeapException
        value_to_return = self.get_min()

        # if the length of the min_heap is 1, pop and return the first element
        if self.heap.length() == 1:
            return self.heap.pop()

        else:
            # pop the last element in the heap and set it to the first element
            self.heap.set_at_index(0, self.heap.pop())

            heap_length = self.heap.length()

            # initialize the parent_index and node to the first element of the min_heap
            parent_index = 0
            parent_node = self.heap.get_at_index(parent_index)

            # loop over the min_heap, percolating the first element into the correct position
            while parent_index < self.heap.length():

                # calculate indices of the parent's left and right children
                left_child_index = parent_index * 2 + 1
                right_child_index = parent_index * 2 + 2

                # initialize the left and right nodes to none
                left_child_node = None
                right_child_node = None

                # if the left_child_index is in the min_heap, initialize the left_child node
                if left_child_index < heap_length:
                    left_child_node = self.heap.get_at_index(left_child_index)

                # do the same for the right_child
                if right_child_index < heap_length:
                    right_child_node = self.heap.get_at_index(right_child_index)

                # if a left and right child exist, find which is smaller and set the min_node
                # and min_index to that child
                if left_child_node is not None and right_child_node is not None:
                    min_child_node = min(left_child_node, right_child_node)
                    if min_child_node == left_child_node:
                        min_child_index = left_child_index

                    else:
                        min_child_index = right_child_index

                # if only the left child exists, set the min_child_node and index accordingly
                elif left_child_node is not None and right_child_node is None:
                    min_child_node = left_child_node
                    min_child_index = left_child_index

                elif right_child_node is not None and left_child_node is None:
                    min_child_node = right_child_node
                    min_child_index = right_child_index

                # if neither left nor right children exist, return
                else:
                    return value_to_return

                # if the parent_node > min_child_node, swap and update parent_index and parent_node
                if parent_node > min_child_node:
                    self.heap.swap(parent_index, min_child_index)
                    parent_index = min_child_index
                    parent_node = self.heap.get_at_index(parent_index)
                    heap_length = self.heap.length()

                else:
                    return value_to_return


    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives a dynamic array with objects in any order and builds a proper MinHeap from them.
        Current content of the MinHeap is lost.
        """
        # reset self.heap to an empty array O(1) runtime
        self.heap = DynamicArray()

        # copy each element of da to self.heap - O(n) runtime
        for i in range(da.length()):
            self.heap.append(da.get_at_index(i))

        heap_length = self.heap.length()

        if heap_length == 1:
            return

        else:

            # set src_index to the first non-leaf node
            first_non_leaf_index = heap_length // 2 - 1

            # loop over the indices from the first non_leaf_index to zero in reverse order
            for index in range(first_non_leaf_index, -1, -1):

                parent_index = index
                parent_node = self.heap.get_at_index(parent_index)

                while parent_index < heap_length:

                    # calculate indices of the parent's left and right children
                    left_child_index = parent_index * 2 + 1
                    right_child_index = parent_index * 2 + 2

                    # initialize the left and right nodes to none
                    left_child_node = None
                    right_child_node = None

                    # if the left_child_index is in the min_heap, initialize the left_child node
                    if left_child_index < heap_length:
                        left_child_node = self.heap.get_at_index(left_child_index)

                    # do the same for the right_child
                    if right_child_index < heap_length:
                        right_child_node = self.heap.get_at_index(right_child_index)

                    # if a left and right child exist, find which is smaller and set the min_node
                    # and min_index to that child
                    if left_child_node is not None and right_child_node is not None:
                        min_child_node = min(left_child_node, right_child_node)
                        if min_child_node == left_child_node:
                            min_child_index = left_child_index

                        else:
                            min_child_index = right_child_index

                    # if only the left child exists, set the min_child_node and index accordingly
                    elif left_child_node is not None and right_child_node is None:
                        min_child_node = left_child_node
                        min_child_index = left_child_index

                    elif right_child_node is not None and not left_child_node is None:
                        min_child_node = right_child_node
                        min_child_index = right_child_index

                    # if neither the left nor right children exist, we are at a leaf node, break
                    else:
                        break

                    # if the parent_node > min_child_node, swap and update parent_index and parent_node
                    if parent_node > min_child_node:
                        self.heap.swap(parent_index, min_child_index)
                        parent_index = min_child_index
                        parent_node = self.heap.get_at_index(parent_index)

                    # if no swaps need to be made, we have found the correct position and can break
                    else:
                        break



# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)


    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())


    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())


    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([5,3,1,2,18,15,20,0,40,15,13])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
