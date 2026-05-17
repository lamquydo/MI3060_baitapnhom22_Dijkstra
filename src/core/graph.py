from dataclasses import dataclass


@dataclass
class Node:
    id: str
    label: str        
    x: float          
    y: float
    node_type: str # "building" hoặc "waypoint"


@dataclass
class Edge:
    source: str       
    target: str
    weight: float     


class Graph:
    def __init__(self):
        # Lưu thông tin đỉnh: { id: Node }
        self.nodes: dict[str, Node] = {}
        # Danh sách cạnh gốc (để UI có thể duyệt)
        self.edges: list[Edge] = []
        # Danh sách kề: { source_id: { target_id: weight } }
        self.adjacency: dict[str, dict[str, float]] = {}

    def __iter__(self):
        # Cho phép duyệt trực tiếp graph để lấy danh sách id đỉnh.
        return iter(self.nodes)

    def add_node(self, node: Node):
        self.nodes[node.id] = node
        # Luôn tạo bucket kề rỗng để tránh phải kiểm tra tồn tại ở nơi khác.
        if node.id not in self.adjacency:
            self.adjacency[node.id] = {}

    def add_edge(self, edge: Edge):
        # Đảm bảo source và target đã tồn tại trong nodes
        if edge.source not in self.nodes or edge.target not in self.nodes:
            missing = [n for n in (edge.source, edge.target) if n not in self.nodes]
            raise KeyError(f"Node not found: {', '.join(missing)}")

        if not isinstance(edge.weight, (int, float)):
            raise TypeError("Edge weight must be a number")

        if edge.weight < 0:
            raise ValueError("Dijkstra does not support negative edge weights")

        self.edges.append(edge)

        # Thêm chiều từ source đến target
        self.adjacency[edge.source][edge.target] = edge.weight

        # Thêm chiều ngược lại (Tính chất vô hướng)
        self.adjacency[edge.target][edge.source] = edge.weight

    def get_neighbors(self, node_id):
        return self.adjacency.get(node_id, {})

    def get_node(self, node_id):
        return self.nodes.get(node_id)