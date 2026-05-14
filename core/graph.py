class Graph:
    def __init__(self):
        # Lưu thông tin đỉnh: { id: {'label': str, 'x': int, 'y': int} }
        self.nodes = {}
        # Danh sách kề: { source_id: { target_id: weight } }
        self.edges = {}

    def __iter__(self):
        # Cho phép duyệt trực tiếp graph để lấy danh sách id đỉnh.
        return iter(self.nodes)

    def add_node(self, node_id, label, x, y):
        self.nodes[node_id] = {
            "label": label,
            "x": x,
            "y": y,
        }
        # Luôn tạo bucket kề rỗng để tránh phải kiểm tra tồn tại ở nơi khác.
        if node_id not in self.edges:
            self.edges[node_id] = {}

    def add_edge(self, u, v, weight):
        # Đảm bảo u và v đã tồn tại trong nodes
        if u not in self.nodes or v not in self.nodes:
            missing_nodes = [node_id for node_id in (u, v) if node_id not in self.nodes]
            raise KeyError(f"Node(s) not found: {', '.join(missing_nodes)}")

        if not isinstance(weight, (int, float)):
            raise TypeError("Edge weight must be a number")

        # Ràng buộc dữ liệu để đảm bảo Dijkstra luôn đúng.
        if weight < 0:
            raise ValueError("Dijkstra does not support negative edge weights")

        # Thêm chiều từ u đến v
        if u not in self.edges:
            self.edges[u] = {}
        self.edges[u][v] = weight

        # Thêm chiều ngược lại từ v đến u (Tính chất vô hướng)
        if v not in self.edges:
            self.edges[v] = {}
        self.edges[v][u] = weight

    def get_neighbors(self, node_id):
        return self.edges.get(node_id, {})

    def get_node_info(self, node_id):
        return self.nodes.get(node_id)