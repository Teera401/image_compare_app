import sys
from PySide6.QtWidgets import QApplication

from modules.image_viewer import ImageCompareViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    viewer = ImageCompareViewer("images_a", "images_b")
    viewer.show()

    sys.exit(app.exec())