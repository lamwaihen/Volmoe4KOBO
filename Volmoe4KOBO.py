import sys
from PyQt5 import QtWidgets, QtGui, QtCore
#from PyQt5.QtGui import QPixmap
from UI.Main import Ui_MainWindow

from ebook import eBook

import os
from shutil import copyfile, rmtree
from tempfile import gettempdir

import io
from PIL.ImageQt import ImageQt

class MainWindow(QtWidgets.QMainWindow):
    books = []
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Palette
        paletteBase = QtGui.QPalette()
        paletteBase.setBrush(self.backgroundRole(), QtGui.QColor(107, 163, 163))
        palette1 = QtGui.QPalette()
        palette1.setBrush(self.backgroundRole(), QtGui.QColor(190, 219, 219))
        palette2 = QtGui.QPalette()
        palette2.setBrush(self.backgroundRole(), QtGui.QColor(149, 193, 193))
        palette3 = QtGui.QPalette()
        palette3.setBrush(self.backgroundRole(), QtGui.QColor(76, 141, 141))
        palette4 = QtGui.QPalette()
        palette4.setBrush(self.backgroundRole(), QtGui.QColor(50, 122, 122))
        self.setPalette(palette1)

        self.ui.toolBox.currentChanged.connect(self.showCurrentPage)
        self.ui.buttonBeginNext.clicked.connect(self.nextButtonClicked)
        self.ui.buttonExtractNext.clicked.connect(self.nextButtonClicked)
        self.ui.buttonEnhancePageNext.clicked.connect(self.nextButtonClicked)
        self.ui.buttonSelectFile.clicked.connect(self.openFileDialog)

        # pageFirstPage
        self.ui.buttonFirstPageNext.clicked.connect(self.nextButtonClicked)        
        self.ui.spinBoxFirstPage.valueChanged.connect(self.firstPagePreviewChanged)

        # pageImageEnhance
        self.ui.spinBoxEnhancePage.valueChanged.connect(self.imageEnhancePreviewChanged)
        self.ui.sliderContrast.valueChanged.connect(self.imageEnhancePreviewChanged)

        self.ui.toolBox.setCurrentIndex(0)
        self.tmp = os.path.join(gettempdir(), "ebook")

    def closeEvent(self, event):
        rmtree(self.tmp, ignore_errors=True)

    def showEvent(self, event):    
        if not os.path.exists(self.tmp):
            os.makedirs(self.tmp)

    def openFileDialog(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"KOBO ePub (*.kepub.epub)")
        _, filename = os.path.split(path[0])
        # Copy selected file to temp folder for further process.
        tempFile = os.path.join(self.tmp, filename)
        copyfile(path[0], tempFile)

        book = eBook(tempFile)
        self.books.append(book)

    def nextButtonClicked(self):
        x = self.ui.toolBox.currentIndex()
        self.ui.toolBox.setCurrentIndex(x+1)

    def showCurrentPage(self):
        #x = self.ui.toolBox.currentIndex()
        #self.ui.stackedWidget.setCurrentIndex(x)

        currentPage = self.ui.stackedWidget.currentWidget().objectName()
        if currentPage == 'pageExtract':
            for book in self.books:
                book.extract()
                book.parse()
        elif currentPage == 'pageFirstPage':
            self.ui.spinBoxFirstPage.setValue(3)
        elif currentPage == 'pageImageEnhance':
            for book in self.books:
                book.layout_fix(self.ui.spinBoxFirstPage.value())
            self.ui.spinBoxEnhancePage.setValue(5)
        elif currentPage == 'pageTOC':
            for book in self.books:
                print("hello")
        elif currentPage == 'pageUpload':
            for book in self.books:
                book.image_enhance(self.ui.sliderContrast.value())

    def firstPagePreviewChanged(self):
        for book in self.books:
            i = self.ui.spinBoxFirstPage.value()
            image = book.get_page(i)
            pixmap = QtGui.QPixmap(image)
            print(pixmap.width(),pixmap.height())
            self.ui.imageFirstPage.setPixmap(pixmap)
    
    def imageEnhancePreviewChanged(self):
        for book in self.books:
            i = self.ui.spinBoxEnhancePage.value()
            image = book.get_page(i)
            self.ui.imageEnhanceLeft.setPixmap(QtGui.QPixmap(image))
            self.ui.imageEnhanceLeft.setScaledContents(True)

            c = self.ui.sliderContrast.value()
            newImage = book.get_enhance_page(i, c)
            self.ui.imageEnhanceRight.setPixmap(pil2pixmap(newImage))
            self.ui.imageEnhanceRight.setScaledContents(True)

def pil2pixmap(image):
    bytes_img = io.BytesIO()
    image.save(bytes_img, format='JPEG')

    qimg = QtGui.QImage()
    qimg.loadFromData(bytes_img.getvalue())

    return QtGui.QPixmap.fromImage(qimg)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())