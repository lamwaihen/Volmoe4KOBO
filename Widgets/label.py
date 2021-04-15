import sys
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import io
from PIL import Image
from PIL.ImageQt import ImageQt

class ImageWidget(QLabel):
    """ Override QLabel to show image that keep aspect ratio, using the given pixmap. """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(False)

        self.labelAR = 1.
        self.imageAR = 1.
        self.oriPixmap = None

    def setPixmap(self, pixmap: QPixmap = None, image: Image = None):
        if image and not pixmap:
            pixmap = self.__pil2Pixmap(image)
        self.labelAR = float(self.width()) / self.height()
        self.imageAR = float(pixmap.width()) / pixmap.height()
        self.oriPixmap = pixmap
        QLabel.setPixmap(self, self.__scaleImage(pixmap))

    def resizeEvent(self, event):
        self.labelAR = float(self.width()) / self.height()
        if self.oriPixmap:
            QLabel.setPixmap(self, self.__scaleImage(self.oriPixmap))
        
    def __scaleImage(self, pixmap: QPixmap) -> QPixmap:
        """ Set a scaled pixmap to a w x h window keeping its aspect ratio 
        Parameters
        ----------
        pixmap : QPixmap
            Input pixmap       
        """
        if pixmap:
            # Get aspect ratio from current widget size.
            labelAR = float(self.width()) / self.height()
            if labelAR > self.imageAR:
                nw = self.height() * self.imageAR
                nh = self.height()
            elif labelAR < self.imageAR:
                nw = self.width()
                nh = self.width() / self.imageAR

            return pixmap.scaled(nw, nh, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            return None

    def __pil2Pixmap(self, image: Image) -> QPixmap:
        """ Convert PIL image to QPixmap """
        bytes_img = io.BytesIO()
        image.save(bytes_img, format='JPEG')

        qimg = QImage()
        qimg.loadFromData(bytes_img.getvalue())

        return QPixmap.fromImage(qimg)