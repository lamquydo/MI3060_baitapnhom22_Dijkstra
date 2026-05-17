from PyQt5.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsLineItem
)
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt


# Màu các Node trên map
NODE_COLORS = {
    "default":  QColor("#ecf0f1"),
    "start":    QColor("#1f78d1"),
    "end":      QColor("#e74c3c"),
    "current":  QColor("#f39c12"),
    "visited":  QColor("#a8e6cf"),
    "path":     QColor("#27ae60"),
}


# Màu các Edge trên map
EDGE_COLORS = {
    "default":   QColor("#95a5a6"),
    "relaxing":  QColor("#f1c40f"),
    "path":      QColor("#27ae60"),
}

BUILDING_RADIUS = 11
WAYPOINT_RADIUS = 1


# NodeItem – hình tròn đại diện cho 1 đỉnh trên bản đồ
class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, label, x, y, node_type="building"):
        radius = BUILDING_RADIUS if node_type == "building" else WAYPOINT_RADIUS
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.node_id = node_id
        self.label_text = label
        self.node_type = node_type

        self.setPos(x, y)
        self.setZValue(10)

        # Giao diện mặc định
        self.setBrush(QBrush(NODE_COLORS["default"]))
        self.setPen(QPen(Qt.NoPen))


        self.setToolTip(f"{label}  ({node_id})")
        self._state = "default"

    def set_state(self, state):
        # Đổi màu node theo trạng thái Dijkstra
        self._state = state
        fill = NODE_COLORS.get(state, NODE_COLORS["default"])
        self.setBrush(QBrush(fill))
        self.setPen(QPen(Qt.NoPen))


# EdgeItem – đường nối giữa 2 đỉnh
class EdgeItem(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, weight, edge_key):
        super().__init__(x1, y1, x2, y2)
        self.edge_key = edge_key  # tuple(sorted([u, v]))
        self.weight = weight
        self.setZValue(5)

        # Giao diện mặc định
        self.setPen(QPen(EDGE_COLORS["default"], 4, Qt.SolidLine, Qt.RoundCap))
        self._state = "default"

    def set_state(self, state):
        # Đổi màu/độ dày edge theo trạng thái Dijkstra.
        self._state = state
        color = EDGE_COLORS.get(state, EDGE_COLORS["default"])
        width = {"default": 4, "relaxing": 5, "path": 8}.get(state, 4)
        self.setPen(QPen(color, width, Qt.SolidLine, Qt.RoundCap))
