from PySide6.QtWidgets import QCheckBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPainter, QPen, QPixmap
from PySide6.QtCore import QPoint, QRectF, Qt


class ZoomableImageView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.isMarkBoder = False
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        
        self.scene.addItem(self.pixmap_item)

        # self.setRenderHints(self.renderHints() | Qt.SmoothTransformation)
        self.setRenderHints(self.renderHints() | QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        # self.setDragMode(QGraphicsView.RubberBandDrag)
        
        self.zoom_factor = 1.25
        self.origin = QPoint()
        self.rubber_rect_item = None
        self.setMouseTracking(True)

    def setMaskborderMode(self, state:bool):
        self.isMarkBoder = state
        self.setDragMode(QGraphicsView.RubberBandDrag) if state else self.setDragMode(QGraphicsView.ScrollHandDrag)

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
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)



    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_factor, self.zoom_factor)
        else:
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)


    def mousePressEvent(self, event):
        if not self.isMarkBoder:
            super().mousePressEvent(event)
        else:
            if event.button() == Qt.LeftButton:
                self.origin = event.pos()

                if self.rubber_rect_item:
                    self.scene.removeItem(self.rubber_rect_item)

                self.rubber_rect_item = self.scene.addRect(
                    QRectF(), QPen(Qt.red, 2)
                )

    def mouseMoveEvent(self, event):
        if  not self.isMarkBoder:
            super().mouseMoveEvent(event)  
        else:      
            if self.rubber_rect_item:
                rect = QRectF(
                    self.mapToScene(self.origin),
                    self.mapToScene(event.pos())
                ).normalized()

                self.rubber_rect_item.setRect(rect)

    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton and self.rubber_rect_item:
    #         rect = self.rubber_rect_item.rect()

    #         print("Selected rect (scene coords):", rect)

    #         # Convert to image coordinates
    #         pixmap = self.pixmap_item.pixmap()

    #         x = int(rect.x())
    #         y = int(rect.y())
    #         w = int(rect.width())
    #         h = int(rect.height())

    #         cropped = pixmap.copy(x, y, w, h)

    #         cropped.save("cropped.png")
    #         print("Saved cropped.png")

    #         # Optional: remove selection box
    #         self.scene.removeItem(self.rubber_rect_item)
    #         self.rubber_rect_item = None