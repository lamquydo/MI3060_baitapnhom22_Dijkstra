import sys

from PyQt5.QtWidgets import QApplication

from src.core.campus_data import load_data
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Load dữ liệu đồ thị từ JSON
    graph = load_data()

    # Tạo và hiển thị cửa sổ chính
    window = MainWindow(graph)
    window.show()

    # Căn giữa màn hình
    screen = window.screen() or app.primaryScreen()
    if screen is not None:
        frame = window.frameGeometry()
        frame.moveCenter(screen.availableGeometry().center())
        window.move(frame.topLeft())

    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
