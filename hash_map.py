# Course: CS261 - Data Structures
# Assignment: 5
# Student: Brian Rud
# Description: An implementation of the hash map ADT


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *

def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash

class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the contents of the hash table without changing the underlying hash table
        capacity
        """
        # loop over each bucket and point the linked list to None
        for i in range(self.capacity):

            self.buckets.get_at_index(i).head = None

        self.size = 0

        return

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.  If the key is not in the map, the
        method returns None
        """
        # hash the key
        hashed_key = self.hash_function(key) % self.capacity

        # get the bucket corresponding to the hashed key
        bucket = self.buckets.get_at_index(hashed_key)

        # return the value associated with the key, or None if the key does
        # not exist in the bucket.
        try:
            return bucket.contains(key).value
        except AttributeError:
            return None

    def put(self, key: str, value: object) -> None:
        """
        Hashes the key value and appends the value object to the linked
        list in the appropriate bucket.
        """

        # hash the key and get the remainder to find the bucket to put the value in
        hash_index = self.hash_function(key) % self.capacity

        # get the bucket in which to put the key/value
        bucket = self.buckets.get_at_index(hash_index)

        # remove the value with the specified key.  If the function
        # returns False then increment the size of the linked list
        if not bucket.remove(key):
            self.size += 1

        # insert the new value
        bucket.insert(key, value)

        return

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.  If the key
        is not in the hash map, the method does nothing, no exception needs to be raised
        """

        # hash the key and get the remainder to find the bucket to put the value in
        hash_index = self.hash_function(key) % self.capacity

        # get the bucket in which to put the key/value
        bucket = self.buckets.get_at_index(hash_index)

        # remove the key/value
        bucket.remove(key)
        self.size -= 1

        return

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise
        it returns False
        """
        # hash the key
        hashed_key = self.hash_function(key) % self.capacity

        # if linked list that the bucket points to contains the key, return True
        # otherwise return false
        if self.buckets.get_at_index(hashed_key).contains(key):
            return True

        else:
            return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        # variable to keep track of the number of empty buckets
        num_empty = 0

        # loop over the buckets in the hash table
        for i in range(self.capacity):

            # if the linked list has no nodes, increment num_empty
            if self.buckets.get_at_index(i).head is None:
                num_empty += 1

        return num_empty

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table
        """
        return self.size/self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Increases the capacity of the hash table.  All existing key/value pairs must remain
        in the new hash map and all hash table links must be rehashed
        """

        if new_capacity < 1:
            return

        nodes_to_hash = DynamicArray()

        # append empty LinkedList objects to the hash table
        if new_capacity > self.capacity:

            for _ in range(new_capacity - self.capacity + 1):
                self.buckets.append(LinkedList())

        # loop over the old buckets
        for index in range(self.capacity):

            curr_bucket = self.buckets.get_at_index(index)

            # loop over each node, storing the a new node with the same key and value
            # in nodes_to_hash
            for node in curr_bucket:

                if node is not None:
                    nodes_to_hash.append(SLNode(node.key, node.value))
                    self.remove(node.key)

        # update the capacity
        self.capacity = new_capacity

        # rehash the nodes
        for index in range(nodes_to_hash.length()):
            curr_node = nodes_to_hash.get_at_index(index)
            self.put(curr_node.key, curr_node.value)

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all the keys stored in the hash map.
        """
        key_array = DynamicArray()

        # loop over the buckets
        for index in range(self.buckets.length()):

            curr_bucket = self.buckets.get_at_index(index)

            # loop over the nodes in the bucket
            for node in curr_bucket:

                # append the key to the DynamicArray
                key_array.append(node.key)

        return key_array

        return DynamicArray()


# # BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
