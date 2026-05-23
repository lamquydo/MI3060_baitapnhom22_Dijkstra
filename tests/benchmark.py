import time
import tracemalloc
import random
from src.core.graph import Graph, Node, Edge
from src.core.dijkstra import dijkstra_steps

def generate_stress_graph(num_nodes, num_edges):
    """Hàm sinh đồ thị ngẫu nhiên quy mô lớn để test áp lực"""
    g = Graph()
    for i in range(num_nodes):
        g.add_node(Node(f"n_{i}", f"Node {i}", random.random()*100, random.random()*100, "waypoint"))
    
    edges_count = 0
    while edges_count < num_edges:
        u = f"n_{random.randint(0, num_nodes-1)}"
        v = f"n_{random.randint(0, num_nodes-1)}"
        if u != v:
            try:
                g.add_edge(Edge(u, v, random.randint(10, 100)))
                edges_count += 1
            except KeyError:
                continue
    return g

def profile_performance(num_nodes, num_edges):
    # Sinh đồ thị áp lực
    g = generate_stress_graph(num_nodes, num_edges)
    
    # Đo bộ nhớ và thời gian
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # Chạy thuật toán tìm đường xuyên suốt đồ thị từ nút đầu đến nút cuối
    generator = dijkstra_steps(g, "n_0", f"n_{num_nodes-1}")
    for _ in generator:
        pass # Chạy hết các bước của generator
        
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    exec_time = end_time - start_time
    memory_used = peak / 1024 # Đổi sang KB
    
    return exec_time, memory_used

# Thực hiện đo đạc trên các quy mô khác nhau
scenarios = [
    ("Quy mô Nhỏ (Mẫu)", 5, 10),
    ("Quy mô Trung bình (HUST thực tế)", 50, 120),
    ("Quy mô Lớn (Stress test)", 500, 1500)
]

print(f"{'Kịch bản kiểm thử':<35} | {'Thời gian chạy (s)':<20} | {'Bộ nhớ đỉnh (KB)':<15}")
print("-" * 76)
for name, nodes, edges in scenarios:
    t, m = profile_performance(nodes, edges)
    print(f"{name:<35} | {t:.6f}s {'':<11} | {m:.2f} KB")