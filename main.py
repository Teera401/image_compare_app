import sys
from PySide6.QtWidgets import QApplication

from modules.image_viewer import ImageCompareViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    viewer = ImageCompareViewer()
    viewer.show()

    sys.exit(app.exec())