from pathlib import Path

from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtCore import QTimer

from .map_view import MapView
from .control_panel import ControlPanel


class MainWindow(QWidget):
    """
    Cửa sổ chính, kết nối MapView, ControlPanel và thuật toán Dijkstra.
    """

    SPEED_MAP = {0: 2000, 1: 1000, 2: 667, 3: 500, 4: 200, 5: 100}

    def __init__(self, graph):
        super().__init__()
        self.setWindowTitle("HUST MAP — Dijkstra Simulation")
        self.setFixedSize(1430, 910)

        self.graph = graph

        # UI components
        self.map_view = MapView(self)
        self.control_panel = ControlPanel(self)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.map_view, stretch=1)
        layout.addWidget(self.control_panel)

        # Load map
        data_dir = Path(__file__).resolve().parent.parent.parent / "data"
        self.map_view.load_background(data_dir / "maphust.png")
        self.map_view.load_graph(self.graph)

        # Populate combo boxes – chỉ hiện building, không hiện waypoint
        node_list = [
            (nid, node.label)
            for nid, node in self.graph.nodes.items()
            if node.node_type == "building"
        ]
        self.control_panel.populate_nodes(node_list)

        # Timer cho animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timer_tick)
        self.speed_ms = self.SPEED_MAP.get(1, 1000)

        # State machine
        self.generator = None
        self.state = "IDLE"  # IDLE | RUNNING | PAUSED | FINISHED
        self._start_id = None
        self._end_id = None

        # Connect signals
        self.control_panel.run_clicked.connect(self._on_run)
        self.control_panel.clear_clicked.connect(self._on_reset)
        self.control_panel.pause_clicked.connect(self._on_pause)
        self.control_panel.continue_clicked.connect(self._on_continue)
        self.control_panel.step_clicked.connect(self._on_step)
        self.control_panel.speed_changed.connect(self._on_speed_changed)

    def _on_run(self):
        # Import ở đây để tránh circular import
        from src.core.dijkstra import dijkstra_steps

        self._start_id = self.control_panel.get_start_id()
        self._end_id = self.control_panel.get_end_id()

        if self._start_id is None or self._end_id is None:
            return

        # Reset trước khi chạy mới
        self.map_view.reset_all()
        self.control_panel.reset_status()

        # Nếu điểm đầu trùng điểm cuối
        if self._start_id == self._end_id:
            self.map_view.highlight_node(self._start_id, "start")
            self.control_panel.show_same_point()
            self.state = "FINISHED"
            return

        # Highlight start/end
        self.map_view.highlight_node(self._start_id, "start")
        self.map_view.highlight_node(self._end_id, "end")

        # Tạo generator
        self.generator = dijkstra_steps(self.graph, self._start_id, self._end_id)
        self.state = "RUNNING"
        self.timer.start(self.speed_ms)

    def _on_timer_tick(self):
        self._advance_one_step()

    def _on_step(self):
        self._advance_one_step()

    def _advance_one_step(self):
        from src.core.dijkstra import trace_path

        if self.generator is None:
            return
        try:
            dstate = next(self.generator)
            self.map_view.apply_dijkstra_state(dstate, self._start_id, self._end_id)
            self.control_panel.update_status(dstate)

            if dstate.phase == "found":
                path = trace_path(dstate.previous, self._start_id, self._end_id)
                self.map_view.show_final_path(path)
                total = dstate.distances.get(self._end_id, 0)
                self.control_panel.show_result(path, total, self.graph)
                self.timer.stop()
                self.state = "FINISHED"
            elif dstate.phase == "no_path":
                self.control_panel.show_no_path()
                self.timer.stop()
                self.state = "FINISHED"
        except StopIteration:
            self.timer.stop()
            self.state = "FINISHED"

    def _on_pause(self):
        self.timer.stop()
        self.state = "PAUSED"

    def _on_continue(self):
        if self.state == "PAUSED" and self.generator is not None:
            self.state = "RUNNING"
            self.timer.start(self.speed_ms)

    def _on_reset(self):
        self.timer.stop()
        self.generator = None
        self.state = "IDLE"
        self.map_view.reset_all()
        self.control_panel.reset_status()

    def _on_speed_changed(self, value):
        self.speed_ms = self.SPEED_MAP.get(value, 1000)
        if self.state == "RUNNING":
            self.timer.setInterval(self.speed_ms)
