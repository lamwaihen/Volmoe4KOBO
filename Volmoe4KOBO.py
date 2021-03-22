import io
import os
import sys
import threading

from shutil import rmtree
from tempfile import gettempdir

from PyQt5 import QtWidgets, QtGui, QtCore
from UI.Main import Ui_MainWindow

from ebook import eBook

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

        # pageBegin
        self.ui.buttonBeginNext.clicked.connect(self.nextButtonClicked)
        self.ui.buttonSelectFile.clicked.connect(self.openFileDialog)

        # pageFirstPage
        self.ui.scrollFirstPage.valueChanged.connect(self.firstPagePreviewChanged)
        self.ui.buttonFirstPageNext.clicked.connect(self.nextButtonClicked)        

        # pageImageEnhance
        self.ui.scrollEnhancePage.valueChanged.connect(self.imageEnhancePreviewChanged)
        self.ui.sliderContrast.valueChanged.connect(self.imageEnhancePreviewChanged)
        self.ui.buttonEnhancePageNext.clicked.connect(self.nextButtonClicked)

        # pageTOC
        self.ui.scrollTOCPage.valueChanged.connect(self.tocPreviewChanged)
        self.ui.buttonTOCPageNext.clicked.connect(self.nextButtonClicked)

        # pageProcess
        self.ui.buttonProcessNext.clicked.connect(self.nextButtonClicked)

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
        #tempFile = os.path.join(self.tmp, filename)
        #copyfile(path[0], tempFile)

        book = eBook(path[0])
        book.extract()
        book.parse()
        self.books.append(book)
        
        # update UI
        self.ui.labelPath.setText(filename)
        self.ui.labelTitle.setText(book.get_info("Title"))
        self.ui.labelAuthor.setText(book.get_info("Author"))
        self.ui.labelPageCount.setText(book.get_info("PageCount"))
        self.ui.imageCover.setPixmap(QtGui.QPixmap(book.get_cover_page()))

        self.ui.buttonBeginNext.setEnabled(True)

    def nextButtonClicked(self):
        x = self.ui.toolBox.currentIndex()
        self.ui.toolBox.setCurrentIndex(x+1)

    def showCurrentPage(self):
        currentPage = self.ui.stackedWidget.currentWidget().objectName()
        if currentPage == 'pageFirstPage':
            for book in self.books:
                size = int(book.get_info("PageCount"))
                self.ui.scrollFirstPage.setRange(1, size)
                self.ui.scrollFirstPage.setValue(3)
        elif currentPage == 'pageImageEnhance':
            for book in self.books:
                book.layout_fix(self.ui.scrollFirstPage.value())
                size = int(book.get_info("PageCount"))
                self.ui.scrollEnhancePage.setRange(1, size)
                self.ui.scrollEnhancePage.setValue(5)
        elif currentPage == 'pageTOC':
            for book in self.books:
                size = int(book.get_info("PageCount"))
                self.ui.scrollTOCPage.setRange(1, size)
                self.ui.scrollTOCPage.setValue(4)
        elif currentPage == 'pageProcess':
            for book in self.books:
                t = threading.Thread(target=fileProcessing, args=(book, self.ui.scrollFirstPage.value(), self.ui.sliderContrast.value()))
                t.start()
        elif currentPage == 'pageUpload':
            for book in self.books:
                print("hello")

    def firstPagePreviewChanged(self):
        for book in self.books:
            i = self.ui.scrollFirstPage.value()
            image = book.get_page(i)
            pixmap = QtGui.QPixmap(image)
            self.ui.imageFirstPage.setPixmap(pixmap)
            self.ui.labelFirstPage.setText(str(i))
    
    def imageEnhancePreviewChanged(self):
        for book in self.books:
            i = self.ui.scrollEnhancePage.value()
            # Get page path
            image = book.get_page(i)
            self.ui.imageEnhanceLeft.setPixmap(QtGui.QPixmap(image))
            self.ui.labelEnhancePage.setText(str(i))

            c = self.ui.sliderContrast.value()
            self.ui.labelContrast.setText(str(c))
            newImage = book.get_enhance_page(i, c)
            self.ui.imageEnhanceRight.setPixmap(image=newImage)

    def tocPreviewChanged(self):
        for book in self.books:
            i = self.ui.scrollTOCPage.value()
            image = book.get_page(i)
            self.ui.imageTOCPage.setPixmap(QtGui.QPixmap(image))
            self.ui.labelTOCPage.setText(str(i))

def fileProcessing(book: eBook, firstPage: int, contrast: int):
    book.image_enhance(contrast)
    book.generate_new_structure(firstPage)
    book.repack()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())