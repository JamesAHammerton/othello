import sys

from PySide6.QtWidgets import QApplication

from ui.launch_window import LaunchWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = LaunchWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
