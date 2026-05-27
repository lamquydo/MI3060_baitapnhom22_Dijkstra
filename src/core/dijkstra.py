from .my_heapq import heappush, heappop
from dataclasses import dataclass

from .graph import Graph

@dataclass
class DijkstraState:
    current_node: str
    visited: set
    distances: dict
    previous: dict
    priority_queue: list
    phase: str  # "exploring" | "found" | "no_path"

def trace_path(previous, start_id, end_id):
    # Hàm phụ trợ để lấy danh sách các node tạo thành đường đi
    path = []
    curr = end_id
    while curr is not None:
        path.append(curr)
        if curr == start_id:
            break
        curr = previous.get(curr)
    return path[::-1] if path[-1] == start_id else []


def dijkstra_steps(graph: Graph, start_id, end_id):
    # Generator - yield từng bước để UI animate được theo hustmap.png
    node_ids = list(graph.nodes.keys())

    if start_id not in node_ids:
        raise KeyError(f"Start node not found: {start_id}")
    if end_id not in node_ids:
        raise KeyError(f"End node not found: {end_id}")

    # Khởi tạo các giá trị ban đầu
    distances = {node: float("inf") for node in node_ids}
    distances[start_id] = 0
    previous = {node: None for node in node_ids}
    visited = set()
    
    # Priority Queue chứa (khoảng cách, node_id)
    pq = [(0, start_id)]

    while pq:
        # Lấy node có khoảng cách nhỏ nhất
        current_dist, u = heappop(pq)

        # Bỏ bản ghi cũ trong heap (đã có đường đi ngắn hơn được cập nhật trước đó).
        if current_dist > distances[u]:
            continue

        # Nếu node đã chốt (visited), bỏ qua
        if u in visited:
            continue

        # Yield bước ĐANG KHÁM PHÁ (exploring)
        # Sao chép dữ liệu để UI đọc trạng thái tức thời mà không bị ảnh hưởng bởi bước sau.
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
        for v, weight in graph.get_neighbors(u).items():
            if v in visited:
                continue
         
            # cập nhật khoảng cách tốt hơn và lưu đỉnh trước đó để truy vết đường đi.
            new_dist = distances[u] + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heappush(pq, (new_dist, v))
                
    # Nếu thoát khỏi vòng lặp mà không tìm thấy đích
    yield DijkstraState(
        current_node="",
        visited=set(visited),
        distances=dict(distances),
        previous=dict(previous),
        priority_queue=[],
        phase="no_path"
    )
