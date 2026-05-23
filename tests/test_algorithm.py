import unittest
from src.core.graph import Graph, Node, Edge
from src.core.dijkstra import dijkstra_steps, trace_path

class TestDijkstraAlgorithm(unittest.TestCase):
    def setUp(self):
        """Khởi tạo một đồ thị mẫu nhỏ để test hộp trắng"""
        self.graph = Graph()
        # Thêm các node biên và node thường
        self.graph.add_node(Node("A", "Toà A", 0, 0, "building"))
        self.graph.add_node(Node("B", "Toà B", 1, 1, "building"))
        self.graph.add_node(Node("C", "Toà C", 2, 2, "building"))
        self.graph.add_edge(Edge("A", "B", 10))
        self.graph.add_edge(Edge("B", "C", 15))
        self.graph.add_edge(Edge("A", "C", 30))

    # 1. White-box Test (Kiểm thử hộp trắng - Đúng logic đường đi ngắn nhất)
    def test_shortest_path_logic(self):
        generator = dijkstra_steps(self.graph, "A", "C")
        final_state = None
        for state in generator:
            final_state = state
        
        self.assertEqual(final_state.phase, "found")
        path = trace_path(final_state.previous, "A", "C")
        # Đường ngắn nhất phải là A -> B -> C (10+15=25) thay vì đi thẳng A -> C (30)
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(final_state.distances["C"], 25)

    # 2. Boundary Test (Kiểm thử giá trị biên)
    def test_same_start_and_end(self):
        """Trường hợp điểm đầu trùng điểm cuối"""
        generator = dijkstra_steps(self.graph, "A", "A")
        final_state = None
        for state in generator:
            final_state = state
        
        self.assertEqual(final_state.phase, "found")
        path = trace_path(final_state.previous, "A", "A")
        self.assertEqual(path, ["A"])
    # 3. Negative Test (Kiểm thử ngoại lệ / Trường hợp lỗi đầu vào)
    def test_negative_edge_weight(self):
        """Kiểm tra hệ thống có chặn việc add cạnh trọng số âm không"""
        with self.assertRaises(ValueError):
            self.graph.add_edge(Edge("A", "C", -5))

    def test_non_existent_node(self):
        """Kiểm tra thuật toán có báo lỗi khi truyền ID không tồn tại"""
        with self.assertRaises(KeyError):
            list(dijkstra_steps(self.graph, "A", "XYZ"))

if __name__ == "__main__":
    unittest.main()