from MinHeap import MinHeap

def test_min_heap():
    print("========== MIN HEAP TEST ==========")

    heap = MinHeap()

    items = [
        (0, 10),
        (1, 5),
        (2, 8),
        (3, 3),
        (4, 7),
        (5, 2)
    ]

    print("\nEnqueuing:")

    for item in items:
        print(f"enqueue {item}")
        heap.enqueue(item)
        heap.print_heap()

    print("\nDequeuing:")

    while not heap.is_empty():
        item = heap.dequeue()
        print(f"dequeue {item}")
        heap.print_heap()


test_min_heap()