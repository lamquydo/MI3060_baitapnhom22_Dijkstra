from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QStyle,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

class ControlPanel(QWidget):
    run_clicked = pyqtSignal()
    clear_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    step_clicked = pyqtSignal()
    speed_changed = pyqtSignal(int)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("controlPanel")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(280)
        self._build_ui()
        self._connect_signals()
        self._apply_styles()
        self._set_paused(False)

    def _build_ui(self):
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(10)

        self.root_layout.addWidget(self._build_title())
        self.root_layout.addWidget(self._build_settings_group())
        self.root_layout.addWidget(self._build_execution_group())
        self.root_layout.addWidget(self._build_speed_group())

        self.root_layout.addStretch()

    def _build_title(self):
        title = QLabel("CONTROL PANEL", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1f78d1;")
        return title

    def _build_settings_group(self):
        settings_group = QGroupBox("Settings", self)
        settings_layout = QFormLayout(settings_group)

        self.start_combo = QComboBox(settings_group)
        self.start_combo.addItems(["Gate", "Library", "Dormitory A", "Student Center"])
        self.destination_combo = QComboBox(settings_group)
        self.destination_combo.addItems(["Library", "Gate", "Dormitory A", "Student Center"])

        start_label = QLabel("Starting Point", settings_group)
        destination_label = QLabel("Destination", settings_group)
        start_label.setStyleSheet("font-size: 16px; font-weight: 480;")
        destination_label.setStyleSheet("font-size: 16px; font-weight: 480;")

        settings_layout.addRow(start_label, self.start_combo)
        settings_layout.addRow(destination_label, self.destination_combo)

        self.run_button = QPushButton("Run Dijkstra", settings_group)
        self.run_button.setObjectName("runButton")

        self.clear_button = QPushButton("Clear/Reset", settings_group)
        self.clear_button.setObjectName("clearButton")

        button_row = QHBoxLayout()
        button_row.addWidget(self.run_button)
        button_row.addWidget(self.clear_button)

        settings_layout.addRow(button_row)
        return settings_group

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
    
    def _connect_signals(self):
        self.run_button.clicked.connect(self._on_run_clicked)
        self.clear_button.clicked.connect(self._on_clear_clicked)
        self.pause_button.clicked.connect(self._on_pause_clicked)
        self.continue_button.clicked.connect(self._on_continue_clicked)
        self.step_button.clicked.connect(self.step_clicked.emit)
        self.speed_slider.valueChanged.connect(self.speed_changed.emit)


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

