import io
import os
import sys

from shutil import copyfile, rmtree
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
        self.resetData()

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
        self.ui.spinFirstPage.valueChanged.connect(self.firstPageSpinChanged)
        self.ui.buttonFirstPageNext.clicked.connect(self.nextButtonClicked)        

        # pageImageEnhance
        self.ui.scrollEnhancePage.valueChanged.connect(self.imageEnhancePreviewChanged)
        self.ui.sliderContrast.valueChanged.connect(self.imageEnhancePreviewChanged)
        self.ui.buttonEnhancePageNext.clicked.connect(self.nextButtonClicked)

        # pageTOC
        self.ui.checkBoxHasTOC.stateChanged.connect(lambda:self.hasTOCChanged(self.ui.checkBoxHasTOC))
        self.ui.scrollTOCPage.valueChanged.connect(self.tocPreviewChanged)
        self.ui.buttonTOCPageNext.clicked.connect(self.nextButtonClicked)

        # pageProcess
        self.ui.buttonProcessNext.clicked.connect(self.nextButtonClicked)

        # pageSave
        self.ui.buttonSaveFile.clicked.connect(self.saveFileButtonClicked)

        self.ui.toolBox.setCurrentIndex(0)

    def closeEvent(self, event):
        rmtree(self.tmp, ignore_errors=True)

    def showEvent(self, event):    
        work_path = settings.value("path/work", os.path.join(gettempdir(), "ebook"))
        if not os.path.exists(work_path):
            os.makedirs(work_path)

    def resetData(self):
        self.file = None
        self.book = None
        self.firstImage = 3 # Assume the 3rd image is the first page
        self.firstPageNum = 1   # And the first page is page 1.
        self.tocPageNum = 3 # Page number of TOC, -1 if not available.

        
    def openFileDialog(self):
        load_path = settings.value("path/load", "C:\\")
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", load_path, "KOBO ePub (*.kepub.epub)")
        # Update settings
        load_path, self.file = os.path.split(path[0])
        settings.setValue("path/load", load_path)

        work_path = settings.value("path/work", os.path.join(gettempdir(), "ebook"))
        self.book = eBook(path[0], work_path)
        self.book.load(self.loadProgressChanged, self.loadCompleted)

    def nextButtonClicked(self):
        x = self.ui.toolBox.currentIndex()
        self.ui.toolBox.setCurrentIndex(x+1)

    def showCurrentPage(self):
        currentPage = self.ui.stackedWidget.currentWidget().objectName()
        if currentPage == 'pageBegin':
            self.ui.progressBarLoad.hide()
        elif currentPage == 'pageFirstPage':
            size = int(self.book.get_info("PageCount"))
            self.ui.scrollFirstPage.setMaximum(size)
            self.ui.scrollFirstPage.setValue(self.firstImage)
        elif currentPage == 'pageImageEnhance':
            self.book.layout_fix(self.ui.scrollFirstPage.value())
            size = int(self.book.get_info("PageCount"))
                self.ui.scrollEnhancePage.setRange(1, size)
                self.ui.scrollEnhancePage.setValue(5)
        elif currentPage == 'pageTOC':
            size = int(self.book.get_info("PageCount"))
            self.ui.scrollTOCPage.setMaximum(size)
            self.ui.scrollTOCPage.setValue(self.tocPageNum)
            self.ui.checkBoxHasTOC.setChecked(True if self.tocPageNum > 0 else False)
        elif currentPage == 'pageProcess':
            self.ui.progressBarSave.hide()
            self.book.save(self.firstImage, self.firstPageNum, self.tocPageNum, self.ui.sliderContrast.value(), self.saveProgressChanged, self.saveCompleted)
        elif currentPage == 'pageSave':
                print("hello")

    def loadProgressChanged(self, value):
        self.ui.progressBarLoad.show()
        self.ui.progressBarLoad.setValue(value)

    def loadCompleted(self):
        #self.book.parse()
        self.books.append(self.book)
        
        # update UI
        self.ui.labelPath.setText("filename")
        self.ui.labelTitle.setText(self.book.get_info("Title"))
        self.ui.labelAuthor.setText(self.book.get_info("Author"))
        self.ui.labelPageCount.setText(self.book.get_info("PageCount"))
        self.ui.imageCover.setPixmap(QtGui.QPixmap(self.book.get_cover_page()))

        self.ui.buttonBeginNext.setEnabled(True)

    def saveProgressChanged(self, value):
        self.ui.progressBarSave.show()
        self.ui.progressBarSave.setValue(value)

    def saveCompleted(self):
        self.ui.buttonProcessNext.setEnabled(True)

    def firstPagePreviewChanged(self):
            i = self.ui.scrollFirstPage.value()
        image = self.book.get_page(i)
            pixmap = QtGui.QPixmap(image)
            self.ui.imageFirstPage.setPixmap(pixmap)
            self.ui.labelFirstPage.setText(str(i))
        # Adjust spin value
        self.ui.spinFirstPage.setValue(max(1, self.firstPageNum + (i - self.firstImage)))
        self.firstImage = i

    def firstPageSpinChanged(self):
        self.firstPageNum = self.ui.spinFirstPage.value()
    
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

    def hasTOCChanged(self, checkbox):
        self.tocPageNum = self.ui.scrollTOCPage.value() if checkbox.isChecked() else -1
        
    def tocPreviewChanged(self):
        for book in self.books:
            i = self.ui.scrollTOCPage.value()
            image = book.get_page(i)
            self.ui.imageTOCPage.setPixmap(QtGui.QPixmap(image))
            self.ui.labelTOCPage.setText(str(i))

    def saveFileButtonClicked(self):        
        save_path = settings.value("path/save", os.path.expanduser("~/Documents"))
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", os.path.join(save_path, self.file), "KOBO ePub (*.kepub.epub)")
        work_path = settings.value("path/work", os.path.join(gettempdir(), "ebook"))
        # Move output file from work folder for to save location.        
        os.replace(os.path.join(work_path, self.file), path[0])
        # Update save path
        save_path, _ = os.path.split(path[0])
        settings.setValue("path/save", save_path)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setOrganizationName("lamwaihen")
    app.setApplicationName("Manga4KOBO")
    app.setApplicationVersion("0.1")

    settings = QtCore.QSettings()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())