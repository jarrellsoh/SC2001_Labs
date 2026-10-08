# Define class for MinHeap, for array representation of a priority queue
# MinHeap accepts a 2-tuple (vertex, distance) as an item, where distance is the sum of weights from start vertex
# Smaller difference = higher priority, thus MinHeap. 

class MinHeap:
    def __init__(self):
        self.heap = []
        self.size = 0
        
    def print_heap(self):
        if self.size == 0:
            print("Heap is empty")
            return
        
        level = 0
        index = 0
        
        while index < self.size:
            level_size = 2 ** level
            end_index = min(index + level_size, self.size)
            
            for i in range(index, end_index):
                print(f"{self.heap[i]}", end="    ")
            print()
            
            index = end_index
            level += 1

    def is_empty(self):
        return self.size == 0

    def enqueue(self, item):
        #Add item to the end of the heap
        self.heap.append(item)
        self.size += 1
        i = self.size - 1
        
        #Repair the heap upwards from newly added item
        while i > 0:
            parent = self._parent(i)
            
            #If parent is less than or equal to item, heap is valid, return
            if self.heap[parent][1] <= item[1]:
                return
            
            #Swap item with parent, update the index and continue
            self.heap[parent], self.heap[i] = self.heap[i], self.heap[parent]
            i = parent

    def dequeue(self):
        #Check for empty heap
        if self.size == 0:
            return None
        
        #Remove minimum item by replacing it with last item
        min_item = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.heap.pop()
        self.size -= 1
        
        #Repair the heap
        self._min_heapify(0)
        
        return min_item

    def peek(self):
        return self.heap[0] if self.size > 0 else None
    
    #----------Private heler methods----------
    
    #Return index of parent, left child and right child
    def _parent(self, i):
        return (i - 1) // 2
    
    def _left(self, i):
        return 2 * i + 1
    
    def _right(self, i):
        return 2 * i + 2
    
    #Recursively repairs heap downwards from the given index i
    def _min_heapify(self, i):
        left = self._left(i)
        right = self._right(i)
        
        #Check if item has children, if not return
        if left >= self.size:
            return
        
        #Determine smaller of the two children
        if right < self.size and self.heap[right][1] < self.heap[left][1]:
            smallest = right
        else:
            smallest = left
           
        #If current node is greater than smaller child, swap and continue heapify 
        if self.heap[smallest][1] < self.heap[i][1]:
            self.heap[smallest], self.heap[i] = self.heap[i], self.heap[smallest]
            self._min_heapify(smallest)