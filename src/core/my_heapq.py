def _sift_up(heap, pos):
    while pos > 0:
        parent_pos = (pos - 1) // 2
        if heap[pos] < heap[parent_pos]:
            heap[pos], heap[parent_pos] = heap[parent_pos], heap[pos]
            pos = parent_pos
        else:
            break

def _sift_down(heap, pos):
    n = len(heap)
    while True:
        smallest = pos
        left_child = 2 * pos + 1
        right_child = 2 * pos + 2
        if left_child < n and heap[left_child] < heap[smallest]:
            smallest = left_child
        if right_child < n and heap[right_child] < heap[smallest]:
            smallest = right_child
        if smallest != pos:
            heap[pos], heap[smallest] = heap[smallest], heap[pos]
            pos = smallest
        else:
            break

def heappush(heap, item):
    heap.append(item)
    _sift_up(heap, len(heap) - 1)

def heappop(heap):
    if not heap:
        raise IndexError("heappop from empty heap")
    last_item = heap.pop()
    if heap:
        return_item = heap[0]
        heap[0] = last_item
        _sift_down(heap, 0)
        return return_item
    return last_item

def heapify(x):
    n = len(x)
    for i in reversed(range(n // 2)):
        _sift_down(x, i)
