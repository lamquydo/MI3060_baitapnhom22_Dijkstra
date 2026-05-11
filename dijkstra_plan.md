# 🗺️ Kế hoạch xây dựng ứng dụng mô phỏng Dijkstra – Bản đồ khuôn viên trường

---

## 1. Lựa chọn thư viện đồ hoạ

### So sánh các lựa chọn phổ biến

| Thư viện | Ưu điểm | Nhược điểm | Phù hợp? |
|---|---|---|---|
| **Pygame** | Nhẹ, vẽ tự do hoàn toàn, dễ animation | Phải tự làm UI | ✅ Tốt cho animation |
| **Tkinter** | Có sẵn trong Python, widget phong phú | Canvas hạn chế, animation lag | ⚠️ Được, nhưng không mượt |
| **PyQt5 / PySide6** | UI chuyên nghiệp, mạnh mẽ | Nặng hơn, learning curve cao | ✅ Tốt cho layout phức tạp |
| **CustomTkinter** | Tkinter đẹp hơn, modern UI | Vẫn hạn chế canvas | ⚠️ Giới hạn |
| **Matplotlib** | Dễ vẽ đồ thị | Không phù hợp animation real-time | ❌ Không phù hợp |

### ✅ Lựa chọn đề xuất: **PyQt5 + QGraphicsScene**

**Lý do:**
- Layout 2 cột (map | control panel) dễ dàng với `QSplitter` / `QHBoxLayout`
- `QGraphicsScene` + `QGraphicsView` hỗ trợ vẽ node, edge, animation mượt
- `QTimer` cho animation từng bước (step-by-step)
- Widget có sẵn: Button, SpinBox, ComboBox, Label, Slider (speed control)
- Dễ scale, zoom bản đồ

**Cài đặt:**
```bash
pip install PyQt5
```

---

## 2. Cấu trúc Project

```
dijkstra_campus/
│
├── main.py                  # Entry point – khởi chạy app
│
├── core/
│   ├── __init__.py
│   ├── graph.py             # Cấu trúc đồ thị (Node, Edge, Graph)
│   ├── dijkstra.py          # Thuật toán Dijkstra (generator-based)
│   └── campus_data.py       # Dữ liệu bản đồ trường (nodes, edges cứng hoặc JSON)
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py       # QMainWindow – layout tổng thể
│   ├── map_view.py          # QGraphicsView + QGraphicsScene – vẽ bản đồ
│   ├── control_panel.py     # QWidget – panel bên phải
│   └── graph_items.py       # QGraphicsItem tuỳ chỉnh (NodeItem, EdgeItem)
│
├── assets/
│   ├── campus_bg.png        # Ảnh nền khuôn viên trường (tuỳ chọn)
│   └── icons/               # Icon cho các nút bấm
│
├── data/
│   └── campus_map.json      # Dữ liệu đồ thị dạng JSON (có thể chỉnh sửa)
│
└── requirements.txt
```

---

## 3. Thiết kế Chi tiết Từng Module

### 3.1 `core/graph.py` – Cấu trúc đồ thị

```python
@dataclass
class Node:
    id: str
    label: str        # "Thư viện", "Ký túc xá A", ...
    x: float          # Toạ độ trên canvas
    y: float

@dataclass  
class Edge:
    source: str       # Node id
    target: str
    weight: float     # Khoảng cách (mét)

class Graph:
    nodes: dict[str, Node]
    adjacency: dict[str, list[(str, float)]]
    
    def add_node(self, node: Node)
    def add_edge(self, edge: Edge)
    def get_neighbors(self, node_id: str) -> list
    def load_from_json(self, path: str)
```

### 3.2 `core/dijkstra.py` – Thuật toán (Generator)

```python
def dijkstra_steps(graph, start_id, end_id):
    """
    Generator – yield từng bước để UI animate được.
    Mỗi bước yield ra DijkstraState:
      - visited: set các node đã xét
      - current: node đang xét
      - distances: dict {node_id: dist}
      - queue: priority queue hiện tại
      - path_so_far: đường đi tạm thời
    """

@dataclass
class DijkstraState:
    current_node: str
    visited: set
    distances: dict
    previous: dict
    priority_queue: list
    phase: str   # "exploring" | "found" | "no_path"
```

**Ưu điểm dùng generator:**  
UI chỉ cần gọi `next(generator)` mỗi lần Step/Timer tick → tách biệt hoàn toàn logic và giao diện.

### 3.3 `ui/map_view.py` – Bản đồ

```
QGraphicsView
  └── QGraphicsScene
        ├── QPixmapItem        ← Ảnh nền campus (tuỳ chọn)
        ├── EdgeItem (x N)     ← Đường nối giữa các node
        │     └── Màu mặc định: xám | đang xét: vàng | đường đi: xanh lá
        └── NodeItem (x N)     ← Các điểm/nút
              └── Chưa xét: trắng | đang xét: cam | visited: xanh nhạt
                  | start: xanh dương | end: đỏ | path: xanh đậm
```

**NodeItem (QGraphicsEllipseItem):**
- Click để chọn điểm đi / điểm đến
- Hiển thị tooltip tên địa điểm
- Đổi màu theo trạng thái Dijkstra

**EdgeItem (QGraphicsLineItem):**
- Hiển thị label trọng số (khoảng cách)
- Đổi màu khi được "relax" hoặc nằm trong đường đi

### 3.4 `ui/control_panel.py` – Panel điều khiển

```
┌─────────────────────────────┐
│  🗺️ DIJKSTRA SIMULATION      │
├─────────────────────────────┤
│ Điểm đi:  [ComboBox ▼]     │
│ Điểm đến: [ComboBox ▼]     │
├─────────────────────────────┤
│  [▶ Start]   [⏸ Pause]     │
│  [▶ Continue] [⏭ Step]     │
│  [🔄 Reset]                 │
├─────────────────────────────┤
│ Tốc độ: [━━●━━━] 500ms      │
├─────────────────────────────┤
│ TRẠNG THÁI                  │
│ Bước: 3/12                  │
│ Đang xét: Thư viện          │
│ Khoảng cách: 350m           │
├─────────────────────────────┤
│ HÀNG ĐỢI (Priority Queue)   │
│  [ListView hiển thị queue]  │
├─────────────────────────────┤
│ KẾT QUẢ                     │
│ A → B → C → D               │
│ Tổng: 850m                  │
└─────────────────────────────┘
```

### 3.5 `data/campus_map.json` – Dữ liệu bản đồ

```json
{
  "nodes": [
    {"id": "lib",  "label": "Thư viện",    "x": 300, "y": 150},
    {"id": "dorm", "label": "Ký túc xá A", "x": 100, "y": 400},
    {"id": "gate", "label": "Cổng chính",  "x": 50,  "y": 600}
  ],
  "edges": [
    {"source": "lib",  "target": "dorm", "weight": 250},
    {"source": "dorm", "target": "gate", "weight": 180}
  ]
}
```

---

## 4. Luồng hoạt động (State Machine)

```
IDLE ──[Start]──► RUNNING ──[Pause]──► PAUSED
  ▲                  │                    │
  │               [Done]              [Continue]──► RUNNING
  │                  │                    │
  └──[Reset]──── FINISHED           [Step]──► PAUSED (bước tiếp)
```

| Nút | IDLE | RUNNING | PAUSED | FINISHED |
|---|---|---|---|---|
| Start | ✅ | ❌ | ❌ | ❌ |
| Pause | ❌ | ✅ | ❌ | ❌ |
| Continue | ❌ | ❌ | ✅ | ❌ |
| Step | ❌ | ❌ | ✅ | ❌ |
| Reset | ❌ | ✅ | ✅ | ✅ |

---

## 5. Animation & Màu sắc

| Đối tượng | Trạng thái | Màu |
|---|---|---|
| Node | Mặc định | ⬜ Trắng viền xám |
| Node | Start | 🔵 Xanh dương |
| Node | End | 🔴 Đỏ |
| Node | Đang xét (current) | 🟠 Cam |
| Node | Đã visited | 🟢 Xanh nhạt |
| Node | Trên đường đi | 💚 Xanh đậm |
| Edge | Mặc định | ── Xám |
| Edge | Đang relax | 🟡 Vàng (pulse) |
| Edge | Đường đi ngắn nhất | 💚 Xanh đậm, dày hơn |

---

## 6. Kế hoạch triển khai (gợi ý)

| Giai đoạn | Nội dung | Thời gian ước tính |
|---|---|---|
| **Phase 1** | `Graph`, `campus_data`, `campus_map.json` | 1–2h |
| **Phase 2** | Dijkstra generator, unit test | 1–2h |
| **Phase 3** | `MapView` – vẽ node/edge tĩnh | 2–3h |
| **Phase 4** | `ControlPanel` – layout + connect signals | 2h |
| **Phase 5** | Kết nối: QTimer + generator + UI update | 2–3h |
| **Phase 6** | Màu sắc, animation, polish | 1–2h |
| **Phase 7** | Thêm ảnh nền, tuning bản đồ trường thật | 1–2h |

**Tổng ước tính: ~10–16 giờ**

---

## 7. Gợi ý mở rộng (sau khi hoàn thiện)

- 🖱️ **Chế độ Edit Map**: kéo thả thêm node/edge
- 💾 **Lưu/Load** bản đồ từ JSON
- 🖼️ **Overlay ảnh vệ tinh** thực tế của trường
- 📊 **So sánh** Dijkstra vs A* vs BFS trực quan
- 🌐 **Web version** với PyScript hoặc chuyển sang React + TypeScript
