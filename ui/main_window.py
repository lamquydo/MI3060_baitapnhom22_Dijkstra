import sys

from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from control_panel import ControlPanel

class MainWindow(QWidget):
    def __init__(self):
        # tạo main window
        super().__init__()
        self.setWindowTitle("HUST MAP")
        self.setFixedSize(1430, 910)

        # tải ảnh map
        self.map_label = QLabel(self)
        self.map_label.setAlignment(Qt.AlignCenter)
        self.original_pixmap = QPixmap("data/maphust.png")
        
        # tạo control panel
        self.control_panel = ControlPanel(self)

        # chỉnh layout
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.map_label)
        layout.addWidget(self.control_panel)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # scale map
        self.update_map_pixmap()
    
    def resizeEvent(self, event):
        self.update_map_pixmap()
        super().resizeEvent(event)

    def update_map_pixmap(self):
        if self.original_pixmap.isNull():
            return

        scaled = self.original_pixmap.scaled(
            self.map_label.size(),
            Qt.KeepAspectRatio
        )

        self.map_label.setPixmap(scaled)
        self.control_panel.setFixedHeight(scaled.height())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    screen = window.screen() or app.primaryScreen()
    if screen is not None:
        frame = window.frameGeometry()
        frame.moveCenter(screen.availableGeometry().center())
        window.move(frame.topLeft())
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
