from src.core.graph import Graph, Node, Edge
from src.core.dijkstra import dijkstra_steps, trace_path

# 1. Khởi tạo dữ liệu gốc (Input Data)
graph = Graph()
graph.add_node(Node("A", "Toà A", 0, 0, "building"))
graph.add_node(Node("B", "Toà B", 1, 1, "building"))
graph.add_node(Node("C", "Toà C", 2, 2, "building"))
graph.add_edge(Edge("A", "B", 10))
graph.add_edge(Edge("B", "C", 15))
graph.add_edge(Edge("A", "C", 30))

print("=============================================")
print("  1. DỮ LIỆU ĐỒ THỊ MẪU NẠP VÀO (INPUT)")
print("=============================================")
print("Các địa điểm: Toà A, Toà B, Toà C")
print("Các tuyến đường kết nối và khoảng cách thực tế:")
print(" - Tuyến A <-> B: 10m")
print(" - Tuyến B <-> C: 15m")
print(" - Tuyến A <-> C: 30m\n")

# 2. Chạy thuật toán và in tiến trình từng bước (Step-by-step Execution)
print("=============================================")
print("  2. TIẾN TRÌNH THUẬT TOÁN DIJKSTRA")
print("=============================================")
generator = dijkstra_steps(graph, "A", "C")
final_state = None

for step in generator:
    print(f"[*] Đang duyệt đỉnh: {step.current_node:<3} | Trạng thái bước: {step.phase:<10} | Khoảng cách tạm thời đến đích C: {step.distances['C']}")
    if step.phase == "found":
        final_state = step

# 3. Kết quả thu được (Output Result)
path = trace_path(final_state.previous, "A", "C")
print("\n=============================================")
print("  3. KẾT QUẢ ĐẦU RA TỐI ƯU (OUTPUT)")
print("=============================================")
print(f"[+] Đường đi ngắn nhất tìm được: {' -> '.join(path)}")
print(f"[+] Tổng chiều dài quãng đường:   {final_state.distances['C']}m")
print("=============================================")