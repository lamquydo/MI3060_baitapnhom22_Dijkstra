from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

from .graph_items import NodeItem, EdgeItem


class MapView(QGraphicsView):
    """
    QGraphicsView hiển thị bản đồ HUST:
    - Ảnh nền maphust.png
    - Overlay NodeItem / EdgeItem
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        # Lưu các item theo id để truy xuất nhanh
        self.node_items: dict[str, NodeItem] = {}
        self.edge_items: dict[tuple, EdgeItem] = {}  # key = tuple(sorted([u,v]))

        # Render đẹp hơn
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.SmoothPixmapTransform
            | QPainter.TextAntialiasing
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("border: none; background: #2c3e50;")

        self._bg_item: QGraphicsPixmapItem | None = None

    # Load map
    def load_background(self, image_path):
        pixmap = QPixmap(str(image_path))
        if pixmap.isNull():
            print(f"[MapView] WARNING: không load được ảnh {image_path}")
            return
        self._bg_item = QGraphicsPixmapItem(pixmap)
        self._bg_item.setZValue(0)
        self._scene.addItem(self._bg_item)
        self._scene.setSceneRect(self._bg_item.boundingRect())

    # Load đồ thị lên scene
    def load_graph(self, graph):
        # Xoá items cũ (nếu reload)
        for item in list(self.node_items.values()):
            self._scene.removeItem(item)
        for item in list(self.edge_items.values()):
            self._scene.removeItem(item)
        self.node_items.clear()
        self.edge_items.clear()

        # Vẽ edges trước
        for edge in graph.edges:
            key = tuple(sorted([edge.source, edge.target]))
            if key in self.edge_items:
                continue  # tránh vẽ trùng cạnh vô hướng
            n1 = graph.get_node(edge.source)
            n2 = graph.get_node(edge.target)
            if n1 is None or n2 is None:
                continue
            item = EdgeItem(n1.x, n1.y, n2.x, n2.y, edge.weight, key)
            item.setVisible(False)  # Ẩn edge lúc IDLE
            self._scene.addItem(item)
            self.edge_items[key] = item

        # Vẽ nodes
        for node_id, node in graph.nodes.items():
            item = NodeItem(node_id, node.label, node.x, node.y, node.node_type)
            self._scene.addItem(item)
            self.node_items[node_id] = item

    # Fit scene vào view khi resize
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._bg_item is not None:
            self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    def showEvent(self, event):
        super().showEvent(event)
        if self._bg_item is not None:
            self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    # API cho MainWindow
    def highlight_node(self, node_id, state):
        item = self.node_items.get(node_id)
        if item:
            item.set_state(state)

    def highlight_edge(self, u, v, state):
        key = tuple(sorted([u, v]))
        item = self.edge_items.get(key)
        if item:
            item.set_state(state)


    def apply_dijkstra_state(self, dstate, start_id, end_id):
        """Cập nhật màu toàn bộ scene theo DijkstraState.
        Ẩn tất cả edges, chỉ hiện những edge đang được duyệt"""

        for item in self.edge_items.values():
            item.setVisible(False)
            item.set_state("default")

        # Hiện + highlight edges thuộc cây đường đi ngắn nhất
        for nid, prev_nid in dstate.previous.items():
            if prev_nid is not None and nid in dstate.visited:
                key = tuple(sorted([nid, prev_nid]))
                if key in self.edge_items:
                    self.edge_items[key].setVisible(True)
                    self.edge_items[key].set_state("relaxing")

        # Cập nhật màu nodes
        for nid, item in self.node_items.items():
            if nid == start_id:
                item.set_state("start")
            elif nid == end_id:
                item.set_state("end")
            elif nid == dstate.current_node:
                item.set_state("current")
            elif nid in dstate.visited:
                item.set_state("visited")
            else:
                item.set_state("default")



    def show_final_path(self, path):
        # Highlight đường đi ngắn nhất, ẩn các cạnh không thuộc path

        # Ẩn tất cả edges trước
        for item in self.edge_items.values():
            item.setVisible(False)

        # Chỉ hiện + highlight edges trên path
        path_keys = set()
        for i in range(len(path) - 1):
            key = tuple(sorted([path[i], path[i + 1]]))
            path_keys.add(key)
            if key in self.edge_items:
                self.edge_items[key].setVisible(True)
                self.edge_items[key].set_state("path")

        # Highlight nodes trên path
        for nid in path:
            item = self.node_items.get(nid)
            if item:
                item.set_state("path")

        # Giữ nguyên start/end markers
        if len(path) >= 1:
            self.highlight_node(path[0], "start")
        if len(path) >= 2:
            self.highlight_node(path[-1], "end")

    def reset_all(self):
        # Reset tất cả node/edge về trạng thái mặc định
        for item in self.node_items.values():
            item.set_state("default")
            item.setToolTip(f"{item.label_text}  ({item.node_id})")
        for item in self.edge_items.values():
            item.set_state("default")
            item.setVisible(False)  # Ẩn edge lúc IDLE
