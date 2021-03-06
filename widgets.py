import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class ImageWidget(QtWidgets.QLabel):
    """ Override QLabel to show image that keep aspect ratio, using the given pixmap. """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(False)

        self.labelAR = 1.
        self.imageAR = 1.
        self.oriPixmap = None

    def setPixmap(self, pixmap):
        self.labelAR = float(self.width()) / self.height()
        self.imageAR = float(pixmap.width()) / pixmap.height()
        self.oriPixmap = pixmap
        QtWidgets.QLabel.setPixmap(self, self.__scaleImage(pixmap))

    def resizeEvent(self, event):
        self.labelAR = float(self.width()) / self.height()
        if self.oriPixmap:
            QtWidgets.QLabel.setPixmap(self, self.__scaleImage(self.oriPixmap))
        
    def __scaleImage(self, pixmap: QtGui.QPixmap) -> QtGui.QPixmap:
        """ Set a scaled pixmap to a w x h window keeping its aspect ratio 
        Parameters
        ----------
        pixmap : QtGui.QPixmap
            Input pixmap       
        """
        if pixmap:
            w = self.width()
            h = self.height()

            labelAR = float(self.width()) / self.height()
            #imageAR = float(self.pixmap().width()) / self.pixmap().height()
            if labelAR > self.imageAR:
                nw = h * self.imageAR
                nh = h
            elif labelAR < self.imageAR:
                nw = w
                nh = w / self.imageAR

            return pixmap.scaled(nw, nh, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        else:
            return None    

#    def hasHeightForWidth(self):
#        return self.pixmap() is not None

#    def heightForWidth(self, w):
#        if self.pixmap():
#            labelAR = float(self.width()) / self.height()
#            imageAR = float(self.pixmap().width()) / self.pixmap().height()
#            if labelAR > imageAR:
#                h = w * imageAR
#            elif labelAR < imageAR:
#                h = self.height()

#            #h = int(w * (self.pixmap().height() / self.pixmap().width()))
#            print("heightForWidth: self {}, {} widget {}, {} pixmap {}, {}".format(self.width(), self.height(), w, h, self.pixmap().width(), self.pixmap().height()))
#            return int(self.height())