from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt


class ZoomableImageView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        # self.setRenderHints(self.renderHints() | Qt.SmoothTransformation)
        self.setRenderHints(self.renderHints() | QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.zoom_factor = 1.25

    def set_image(self, image_path):
        if not image_path:
            self.scene.clear()
            self.pixmap_item = QGraphicsPixmapItem()
            self.scene.addItem(self.pixmap_item)
            return
        pixmap = QPixmap(image_path)
        self.pixmap_item.setPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect())
        self.resetTransform()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_factor, self.zoom_factor)
        else:
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)