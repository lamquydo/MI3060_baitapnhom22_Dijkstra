import json
from pathlib import Path

from .graph import Graph


def _default_data_dir():
    # Chuẩn hóa đường dẫn thư mục data theo vị trí package, không phụ thuộc cwd hiện tại.
    return Path(__file__).resolve().parent.parent / "data"


def _load_json_array(file_path):
    # Mỗi file dữ liệu đều phải là mảng JSON để duyệt tuần tự và nạp vào graph.
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array in {file_path}")
    return data


def load_hust_graph(nodes_file = None, edges_file = None):
    # Cho phép truyền file tùy ý khi test; mặc định dùng dữ liệu trong thư mục data.
    data_dir = _default_data_dir()
    nodes_path = Path(nodes_file) if nodes_file else data_dir / "campus_nodes.json"
    edges_path = Path(edges_file) if edges_file else data_dir / "campus_edges.json"

    raw_nodes = _load_json_array(nodes_path)
    raw_edges = _load_json_array(edges_path)

    hust_map = Graph()

    for node in raw_nodes:
        hust_map.add_node(node["id"], node["label"], node["x"], node["y"])

    for edge in raw_edges:
        hust_map.add_edge(edge["source"], edge["target"], edge["weight"])

    return hust_map
