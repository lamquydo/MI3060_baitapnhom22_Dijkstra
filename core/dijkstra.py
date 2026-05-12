import heapq
from dataclasses import dataclass

@dataclass
class DijkstraState:
    current_node: str
    visited: set
    distances: dict
    previous: dict
    priority_queue: list
    phase: str  # "exploring" | "found" | "no_path"

def trace_path(previous, start_id, end_id):
    """Hàm phụ trợ để lấy danh sách các node tạo thành đường đi"""
    path = []
    curr = end_id
    while curr is not None:
        path.append(curr)
        if curr == start_id:
            break
        curr = previous.get(curr)
    return path[::-1] if path[-1] == start_id else []

def dijkstra_steps(graph, start_id, end_id):
    """
    Generator - yield từng bước để UI animate được theo image_fbe081.png
    """
    # 1. Khởi tạo các giá trị ban đầu
    distances = {node: float('inf') for node in graph}
    distances[start_id] = 0
    previous = {node: None for node in graph}
    visited = set()
    
    # Priority Queue chứa (khoảng cách, node_id)
    pq = [(0, start_id)]

    while pq:
        # Lấy node có khoảng cách nhỏ nhất
        current_dist, u = heapq.heappop(pq)

        # Nếu node đã chốt (visited), bỏ qua
        if u in visited:
            continue

        # Yield bước ĐANG KHÁM PHÁ (exploring)
        yield DijkstraState(
            current_node=u,
            visited=set(visited),
            distances=dict(distances),
            previous=dict(previous),
            priority_queue=list(pq),
            phase="exploring"
        )

        # Nếu đã tìm thấy đích
        if u == end_id:
            visited.add(u)
            yield DijkstraState(
                current_node=u,
                visited=set(visited),
                distances=dict(distances),
                previous=dict(previous),
                priority_queue=list(pq),
                phase="found"
            )
            return

        # Đánh dấu đã chốt node u
        visited.add(u)

        # Duyệt các hàng xóm v của u
        for v, weight in graph.get(u, {}).items():
            if v in visited:
                continue
                
            new_dist = distances[u] + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(pq, (new_dist, v))
                
    # Nếu thoát khỏi vòng lặp mà không tìm thấy đích
    yield DijkstraState(
        current_node="",
        visited=set(visited),
        distances=dict(distances),
        previous=dict(previous),
        priority_queue=[],
        phase="no_path"
    )