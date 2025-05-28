class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LinkedListLRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache_dict = {}
        self.head = None
        self.tail = None
        self.put_miss_count = 0
        self.remove_miss_count = 0
        self.get_miss_count = 0
        self.total_operations = 0

    def insert_at_last(self, key, value):
        new_node = Node(key, value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            a=self.head
            while a.next is not None:
                a=a.next
            a.next=new_node


    def move_to_front(self, node):
        if node == self.head:
            return
        elif node == self.tail:
            node.prev.next = None
            self.tail = node.prev
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        node.next = self.head
        self.head.prev = node
        self.head = node

    def remove_last_node(self):
        if not self.head:
            return None
        removed_node = self.tail
        if not self.head.next:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None

        return removed_node

    def put_item(self, key, value):
        assert 0 <= key <= 100, "Key must be between 0 and 100"
        assert 0 <= value <= 100, "Value must be between 0 and 100"

        self.total_operations += 1
        if key in self.cache_dict:
            node = self.cache_dict[key]
            node.value = value
            self.move_to_front(node)
        else:
            if len(self.cache_dict) >= self.capacity:
                self.remove_miss_count += 1
                removed_node = self.remove_last_node()
                if removed_node:
                    del self.cache_dict[removed_node.key]

            if len(self.cache_dict) < self.capacity:
                self.insert_at_last(key, value)
                self.cache_dict[key] = self.head
                if self.put_miss_count < 50:
                    self.put_miss_count += 1

    def get_item(self, key):
        self.total_operations+= 1
        if key not in self.cache_dict:
            self.get_miss_count += 1
            return None
        else:
            node = self.cache_dict[key]
            self.move_to_front(node)
            return node.value

    def final_miss_rate(self):
        total_miss = self.put_miss_count + self.remove_miss_count + self.get_miss_count
        miss_rate = (total_miss / self.total_operations) * 100
        print(f"The total miss rate of cache is {miss_rate:.2f}%")

    def print_cache(self):
        a = self.head
        while a:
            print(f"({a.key}: {a.value})", end=", ")
            a = a.next
        print("None")
lrucache =LinkedListLRUCache(2)
lrucache.put_item(1, 1)
lrucache.put_item(2, 2)
lrucache.get_item(1)
lrucache.put_item(3, 3)
lrucache.get_item(2)
lrucache.put_item(4, 4)
lrucache.get_item(1)
lrucache.get_item(3)
lrucache.get_item(4)

# Usage
linked_list_lru_cache = LinkedListLRUCache(50)

# Add key-value pairs from 0_49
for i in range(50):
    linked_list_lru_cache.put_item(i, i)
print("key-value pairs from 0_49")
linked_list_lru_cache.print_cache()

# Retrieve odd keys
for i in range(1, 50, 2):
    linked_list_lru_cache.get_item(i)

# Enter prime numbers as keys
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

for i in range(2, 101):
    if is_prime(i):
        linked_list_lru_cache.put_item(i, i)
print("cache with prime numbers:")
linked_list_lru_cache.print_cache()
linked_list_lru_cache.final_miss_rate()