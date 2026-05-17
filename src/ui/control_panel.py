from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QStyle,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class ControlPanel(QWidget):
    # tạo các signal lúc user click button
    run_clicked = pyqtSignal()
    clear_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    step_clicked = pyqtSignal()
    speed_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("controlPanel")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(280)

        # Mapping: combo index → node_id
        self._node_ids: list[str] = []

        self._build_ui()
        self._connect_signals()
        self._apply_styles()
        self._set_paused(False)

    # Build UI
    def _build_ui(self):
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(10)

        self.root_layout.addWidget(self._build_title())
        self.root_layout.addWidget(self._build_settings_group())
        self.root_layout.addWidget(self._build_execution_group())
        self.root_layout.addWidget(self._build_speed_group())
        self.root_layout.addWidget(self._build_status_group())
        self.root_layout.addWidget(self._build_result_group())

        self.root_layout.addStretch()

    # Title
    def _build_title(self):
        title = QLabel("CONTROL PANEL", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1f78d1;")
        return title

    # Settings
    def _build_settings_group(self):
        settings_group = QGroupBox("Settings", self)
        settings_layout = QVBoxLayout(settings_group)

        self.start_combo = QComboBox(settings_group)
        self.destination_combo = QComboBox(settings_group)

        start_label = QLabel("Starting Point", settings_group)
        destination_label = QLabel("Destination", settings_group)
        start_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        destination_label.setStyleSheet("font-size: 14px; font-weight: 600;")

        settings_layout.addWidget(start_label)
        settings_layout.addWidget(self.start_combo)
        settings_layout.addWidget(destination_label)
        settings_layout.addWidget(self.destination_combo)

        self.run_button = QPushButton("Run Dijkstra", settings_group)
        self.run_button.setObjectName("runButton")

        self.clear_button = QPushButton("Clear/Reset", settings_group)
        self.clear_button.setObjectName("clearButton")

        button_row = QHBoxLayout()
        button_row.addWidget(self.run_button)
        button_row.addWidget(self.clear_button)

        settings_layout.addLayout(button_row)
        return settings_group

    # Execution Controls
    def _build_execution_group(self):
        execution_group = QGroupBox("Execution Controls", self)
        execution_layout = QHBoxLayout(execution_group)

        self.pause_button = QPushButton("Pause", execution_group)
        self.pause_button.setObjectName("pauseButton")
        self.pause_button.setCheckable(True)

        self.continue_button = QPushButton("Continue", execution_group)
        self.continue_button.setObjectName("continueButton")
        self.continue_button.setCheckable(True)

        self.step_button = QPushButton("Step", execution_group)
        self.step_button.setObjectName("stepButton")

        execution_layout.addWidget(self.pause_button)
        execution_layout.addWidget(self.continue_button)
        execution_layout.addWidget(self.step_button)

        return execution_group

    # Stimulation Speed Control
    def _build_speed_group(self):
        speed_group = QGroupBox("Simulation Speed", self)
        speed_layout = QVBoxLayout(speed_group)

        speed_label_row = QHBoxLayout()
        speed_label_row.addWidget(QLabel("Slow", speed_group))
        speed_label_row.addStretch()
        speed_label_row.addWidget(QLabel("Fast", speed_group))

        self.speed_slider = QSlider(Qt.Horizontal, speed_group)
        self.speed_slider.setRange(0, 5)
        self.speed_slider.setSingleStep(1)
        self.speed_slider.setPageStep(1)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setValue(1)

        speed_layout.addLayout(speed_label_row)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self._build_speed_ticks_widget(speed_group))
        return speed_group

    # Tạo các speed ticks
    def _build_speed_ticks_widget(self, parent):
        labels_text = ["0.5x", "1x", "1.5x", "2x", "5x", "10x"]
        num = len(labels_text)

        container = QWidget(parent)
        container.setFixedHeight(18)

        labels = []
        for i, text in enumerate(labels_text):
            lbl = QLabel(text, container)
            lbl.setStyleSheet("font-size: 11px;")
            lbl.adjustSize()
            labels.append((i, lbl))

        def reposition(event = None):
            handle_len = self.speed_slider.style().pixelMetric(
                QStyle.PM_SliderLength, None, self.speed_slider
            )
            half_handle = handle_len // 2
            track_w = self.speed_slider.width() - handle_len

            # Tính x_offset
            slider_pos_in_group = self.speed_slider.mapTo(
                self.speed_slider.parent(), self.speed_slider.pos()
            )
            container_pos_in_group = container.mapTo(
                container.parent(), container.pos()
            )
            x_offset = slider_pos_in_group.x() - container_pos_in_group.x() + half_handle

            manual_offsets = {
                0: -5, # 0.5x
                1: 2,  # 1x
                2: -1, # 1.5x
                3: 0,  # 2x
                4: 0,  # 5x
                5: 5   # 10x
            }

            for i, lbl in labels:
                ratio = i / (num - 1)
                center_x = x_offset + ratio * track_w
                lbl_w = lbl.width()

                # Căn lề mặc định
                if i == 0:
                    base_x = int(center_x)
                elif i == num - 1:
                    base_x = int(center_x) - lbl_w
                else:
                    base_x = int(center_x) - lbl_w // 2

                dx = manual_offsets.get(i, 0)
                final_x = base_x + dx
                lbl.move(final_x, 0)

        container.resizeEvent = reposition
        return container

    # Trạng thái thuật toán
    def _build_status_group(self):
        status_group = QGroupBox("State", self)
        layout = QFormLayout(status_group)

        self.status_step_label = QLabel("—", status_group)
        self.status_current_label = QLabel("—", status_group)
        self.status_distance_label = QLabel("—", status_group)

        lbl_step = QLabel("Step:", status_group)
        lbl_current = QLabel("Current:", status_group)
        lbl_dist = QLabel("Distance:", status_group)
        for lbl in (lbl_step, lbl_current, lbl_dist):
            lbl.setStyleSheet("font-weight: 600;")

        layout.addRow(lbl_step, self.status_step_label)
        layout.addRow(lbl_current, self.status_current_label)
        layout.addRow(lbl_dist, self.status_distance_label)

        # Hiển thị hàng đợi ưu tiên
        pq_label = QLabel("Priority Queue:", status_group)
        pq_label.setStyleSheet("font-weight: 600;")
        layout.addRow(pq_label)

        self.pq_list = QListWidget(status_group)
        self.pq_list.setMaximumHeight(100)
        self.pq_list.setStyleSheet("font-size: 12px;")
        layout.addRow(self.pq_list)

        self._step_count = 0
        return status_group

    # Kết quả
    def _build_result_group(self):
        result_group = QGroupBox("Result", self)
        layout = QVBoxLayout(result_group)

        self.result_hint_label = QLabel("Shortest path: green path on the map", result_group)
        self.result_hint_label.setWordWrap(True)
        self.result_hint_label.setStyleSheet("font-size: 12px; color: #555;")
        self.result_hint_label.hide()

        self.result_distance_label = QLabel("—", result_group)
        self.result_distance_label.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #27ae60;"
        )

        layout.addWidget(self.result_hint_label)
        layout.addWidget(self.result_distance_label)
        return result_group

    # Connect signals
    def _connect_signals(self):
        self.run_button.clicked.connect(self._on_run_clicked)
        self.clear_button.clicked.connect(self._on_clear_clicked)
        self.pause_button.clicked.connect(self._on_pause_clicked)
        self.continue_button.clicked.connect(self._on_continue_clicked)
        self.step_button.clicked.connect(self.step_clicked.emit)
        self.speed_slider.valueChanged.connect(self.speed_changed.emit)

    # các hàm xử lí signal
    def _on_run_clicked(self):
        self._set_paused(False)
        self.run_clicked.emit()

    def _on_clear_clicked(self):
        self._set_paused(False)
        self.clear_clicked.emit()

    def _on_pause_clicked(self):
        self._set_paused(True)
        self.pause_clicked.emit()

    def _on_continue_clicked(self):
        self._set_paused(False)
        self.continue_clicked.emit()

    def _set_paused(self, paused):
        self.step_button.setEnabled(paused)
        self.pause_button.setChecked(paused)
        self.continue_button.setChecked(not paused)

    def populate_nodes(self, node_list):
        # Nạp danh sách node vào ComboBox. node_list: list of (node_id, label)
        self._node_ids.clear()
        self.start_combo.clear()
        self.destination_combo.clear()

        for node_id, label in node_list:
            self._node_ids.append(node_id)
            self.start_combo.addItem(label, userData=node_id)
            self.destination_combo.addItem(label, userData=node_id)

    def get_start_id(self):
        return self.start_combo.currentData()

    def get_end_id(self):
        return self.destination_combo.currentData()

    def update_status(self, dstate):
        # Cập nhật panel trạng thái từ DijkstraState
        self._step_count += 1
        self.status_step_label.setText(str(self._step_count))
        self.status_current_label.setText(str(dstate.current_node))

        dist = dstate.distances.get(dstate.current_node, float("inf"))
        dist_text = f"{dist:.0f}m" if dist < float("inf") else "∞"
        self.status_distance_label.setText(dist_text)

        # Cập nhật priority queue
        self.pq_list.clear()
        for d, nid in sorted(dstate.priority_queue):
            self.pq_list.addItem(f"  {nid}  →  {d:.0f}m")

    def show_result(self, path, total_dist, graph):
        # Hiển thị kết quả đường đi ngắn nhất
        self.result_hint_label.show()
        self.result_distance_label.setText(f"Total Distance: {total_dist:.0f}m")

    def show_no_path(self):
        self.result_hint_label.hide()
        self.result_distance_label.setText("No path found!")
        self.result_distance_label.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #e74c3c;"
        )

    def show_same_point(self):
        self.result_hint_label.hide()
        self.result_distance_label.setText("Start and destination are the same!")
        self.result_distance_label.setStyleSheet(
            "font-size: 14px; font-weight: 700; color: #d68910;"
        )

    def reset_status(self):
        # Reset toàn bộ trạng thái về ban đầu
        self._step_count = 0
        self.status_step_label.setText("—")
        self.status_current_label.setText("—")
        self.status_distance_label.setText("—")
        self.pq_list.clear()
        self.result_hint_label.hide()
        self.result_distance_label.setText("—")
        self.result_distance_label.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #27ae60;"
        )

    # Styles for Control Panel
    def _apply_styles(self):
        self.setStyleSheet(
            """
            QWidget#controlPanel {
                background-color: #dce7ea;
            }
            QGroupBox {
                border: 1px solid #b5c4ca;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
                color: #1f78d1;
                font-weight: 700;
            }
            QPushButton {
                min-height: 30px;
                font-size: 14px;
                border: 1px solid #4f6575;
                border-radius: 6px;
            }
            QComboBox {
                min-height: 28px;
                font-size: 14px;
            }
            QPushButton#runButton {
                background-color: #2e8b57;
                color: #ffffff;
            }
            QPushButton#runButton:hover {
                background-color: #45a86f;
            }
            QPushButton#runButton:pressed,
            QPushButton#runButton:checked {
                background-color: #53b57d;
            }
            QPushButton#clearButton {
                background-color: #7f8c8d;
                color: #ffffff;
            }
            QPushButton#clearButton:hover {
                background-color: #95a2a3;
            }
            QPushButton#clearButton:pressed,
            QPushButton#clearButton:checked {
                background-color: #a4b0b1;
            }
            QPushButton#pauseButton {
                background-color: #d68910;
                color: #ffffff;
            }
            QPushButton#pauseButton:hover {
                background-color: #e49f33;
            }
            QPushButton#pauseButton:pressed,
            QPushButton#pauseButton:checked {
                background-color: #f0b55a;
            }
            QPushButton#continueButton {
                background-color: #1f78d1;
                color: #ffffff;
            }
            QPushButton#continueButton:hover {
                background-color: #3790ea;
            }
            QPushButton#continueButton:pressed,
            QPushButton#continueButton:checked {
                background-color: #4ca5ff;
            }
            QPushButton#stepButton {
                background-color: #1f78d1;
                color: #ffffff;
            }
            QPushButton#stepButton:hover:!disabled {
                background-color: #3790ea;
            }
            QPushButton#stepButton:pressed {
                background-color: #4ca5ff;
            }
            QPushButton#stepButton:disabled {
                background-color: #b8c3cc;
                color: #6e7b87;
                border-color: #a8b4bf;
            }
            """
        )
