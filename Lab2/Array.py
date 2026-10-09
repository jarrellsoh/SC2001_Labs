
# Define class for an array-based priority queue
# Items are stored as (vertex, distance) tuples
# Smaller distance = higher priority

class Array:
    def __init__(self):
        self.queue = []
        self.size = 0

    def is_empty(self):
        return self.size == 0

    # Add item to the end of the array
    def enqueue(self, item):
        self.queue.append(item)
        self.size += 1

    # Remove and return item with smallest distance
    def dequeue(self):
        if self.size == 0:
            return None

        min_index = 0

        # Search entire array for minimum distance
        for i in range(1, self.size):
            if self.queue[i][1] < self.queue[min_index][1]:
                min_index = i

        # Remove and return minimum item
        min_item = self.queue.pop(min_index)
        self.size -= 1

        return min_item

    # Return minimum item without removing it
    def peek(self):
        if self.size == 0:
            return None

        min_item = self.queue[0]

        for i in range(1, self.size):
            if self.queue[i][1] < min_item[1]:
                min_item = self.queue[i]

        return min_item
