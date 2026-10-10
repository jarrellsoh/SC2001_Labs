# Define class for an array-based priority queue
# Items are stored as (vertex, distance) tuples
# Smaller distance = higher priority

class Array:
    def __init__(self):
        self.queue = []
        self.size = 0

        # Store the index of each vertex in the array
        self.position = {}

    def is_empty(self):
        return self.size == 0

    # Add item to the end of the array
    def enqueue(self, item):
        vertex, distance = item

        # If vertex already exists, update its distance
        if vertex in self.position:
            self.update(vertex, distance)
            return

        # Add new item to the end of the array
        self.queue.append(item)
        self.position[vertex] = self.size
        self.size += 1

    # Remove and return item with smallest distance
    def dequeue(self):
        # Check for empty queue
        if self.size == 0:
            return None

        min_index = 0

        # Search entire array for minimum distance
        for i in range(1, self.size):
            if self.queue[i][1] < self.queue[min_index][1]:
                min_index = i

        # Remove minimum item
        min_item = self.queue[min_index]
        min_vertex = min_item[0]

        # Replace removed item with last item
        last_item = self.queue[self.size - 1]
        self.queue[min_index] = last_item

        # Update position of moved vertex
        self.position[last_item[0]] = min_index
        self.queue.pop()
        self.size -= 1

        # Remove extracted vertex from position dictionary
        del self.position[min_vertex]

        return min_item

    # Return minimum item without removing it
    def peek(self):
        # Check for empty queue
        if self.size == 0:
            return None

        min_index = 0

        # Find item with smallest distance
        for i in range(1, self.size):
            if self.queue[i][1] < self.queue[min_index][1]:
                min_index = i

        return self.queue[min_index]

    def update(self, vertex, new_distance):
        # Insert vertex if not already in the queue
        if vertex not in self.position:
            self.enqueue((vertex, new_distance))
            return

        # Find vertex using its stored index
        index = self.position[vertex]

        # Update the distance
        self.queue[index] = (vertex, new_distance)
