from graph import Graph

def load_hust_graph():
    hust_map = Graph()

    # Dữ liệu Nodes từ JSON của bạn
    raw_nodes = [
        {"id": "cong_parabol", "label": "Cổng Parabol", "x": 50, "y": 500},
        {"id": "cong_bac", "label": "Cổng Bắc", "x": 350, "y": 50},
        {"id": "cong_b8", "label": "Cổng B8", "x": 750, "y": 550},
        {"id": "c1", "label": "Nhà C1", "x": 350, "y": 120},
        {"id": "c2", "label": "Nhà C2", "x": 250, "y": 250},
        {"id": "c3", "label": "Nhà C3", "x": 500, "y": 200},
        {"id": "c4", "label": "Nhà C4", "x": 500, "y": 300},
        {"id": "c5", "label": "Nhà C5", "x": 500, "y": 400},
        {"id": "c6", "label": "Nhà C6", "x": 650, "y": 300},
        {"id": "c7", "label": "Nhà C7", "x": 650, "y": 400},
        {"id": "c8", "label": "Nhà C8", "x": 650, "y": 500},
        {"id": "c9", "label": "Nhà C9", "x": 250, "y": 400},
        {"id": "c10", "label": "Nhà C10", "x": 500, "y": 480},
        {"id": "d1", "label": "Nhà D1", "x": 420, "y": 620},
        {"id": "d2", "label": "Nhà D2", "x": 220, "y": 680},
        {"id": "d3", "label": "Nhà D3", "x": 650, "y": 620},
        {"id": "d4", "label": "Nhà D4", "x": 180, "y": 780},
        {"id": "d5", "label": "Nhà D5", "x": 650, "y": 700},
        {"id": "d6", "label": "Nhà D6", "x": 300, "y": 750},
        {"id": "d7", "label": "Nhà D7-ITP", "x": 650, "y": 780},
        {"id": "d8", "label": "Nhà D8", "x": 300, "y": 820},
        {"id": "d9", "label": "Nhà D9", "x": 520, "y": 850},
        {"id": "b1", "label": "Nhà B1", "x": 880, "y": 700},
        {"id": "b5", "label": "Nhà B5", "x": 900, "y": 260},
        {"id": "b5b", "label": "Nhà B5b", "x": 900, "y": 220},
        {"id": "b6", "label": "Nhà B6", "x": 800, "y": 260},
        {"id": "b7", "label": "Nhà B7", "x": 800, "y": 340},
        {"id": "b7bis", "label": "Nhà B7bis", "x": 800, "y": 420},
        {"id": "b8", "label": "Nhà B8", "x": 800, "y": 500},
        {"id": "b9", "label": "Nhà B9", "x": 900, "y": 340},
        {"id": "thu_vien", "label": "Thư viện Tạ Quang Bửu", "x": 520, "y": 700},
        {"id": "ho_tien", "label": "Hồ Tiền", "x": 400, "y": 750},
        {"id": "ht", "label": "HT", "x": 500, "y": 140},
        {"id": "cfc", "label": "CFC", "x": 620, "y": 180},
        {"id": "itims", "label": "Viện ITIMS", "x": 420, "y": 480},
        {"id": "lab1", "label": "LAB (gần C6)", "x": 680, "y": 360},
        {"id": "lab2", "label": "LAB (gần C7)", "x": 700, "y": 400},
        {"id": "pc", "label": "PC", "x": 330, "y": 650},
        {"id": "vdz", "label": "VDZ", "x": 380, "y": 640},
        {"id": "cfl", "label": "CFL", "x": 420, "y": 680},
        {"id": "f", "label": "F", "x": 920, "y": 760},
        {"id": "ptn", "label": "PTN", "x": 680, "y": 880}
    ]

    # Dữ liệu Edges từ JSON của bạn
    raw_edges = [
        {"source": "cong_bac", "target": "c1", "weight": 70},
        {"source": "cong_parabol", "target": "c9", "weight": 220},
        {"source": "cong_parabol", "target": "d4", "weight": 300},
        {"source": "c1", "target": "c2", "weight": 160},
        {"source": "c1", "target": "c3", "weight": 170},
        {"source": "c1", "target": "ht", "weight": 150},
        {"source": "ht", "target": "cfc", "weight": 120},
        {"source": "c2", "target": "c9", "weight": 150}
    ]

    # Nạp vào đối tượng hust_map
    for node in raw_nodes:
        hust_map.add_node(node['id'], node['label'], node['x'], node['y'])

    for edge in raw_edges:
        hust_map.add_edge(edge['source'], edge['target'], edge['weight'])

    return hust_map

