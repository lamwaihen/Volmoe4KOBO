import io
import os
import sys

from shutil import move, rmtree
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

        self.ui.stackedWidget.currentChanged.connect(self.showCurrentPage)

        self.ui.buttonSelectFile.clicked.connect(self.openFileDialog)
        self.ui.progressBarLoad.setHidden(True)
        self.ui.labelBookName.setHidden(True)

        self.ui.statusbar.setHidden(True)

        # pageBegin

        # pageBookInfo
        self.ui.buttonBeginNext.clicked.connect(self.nextButtonClicked)

        # pageFirstPage
        self.ui.scrollFirstPage.valueChanged.connect(self.firstPagePreviewChanged)
        self.ui.spinFirstPage.valueChanged.connect(self.firstPageSpinChanged)
        self.ui.buttonFirstPagePrev.clicked.connect(self.prevButtonClicked)
        self.ui.buttonFirstPageNext.clicked.connect(self.nextButtonClicked)

        # pageImageEnhance
        self.ui.scrollEnhancePage.valueChanged.connect(self.imageEnhancePreviewChanged)
        self.ui.sliderContrast.valueChanged.connect(self.imageEnhancePreviewChanged)
        self.ui.buttonEnhancePagePrev.clicked.connect(self.prevButtonClicked)
        self.ui.buttonEnhancePageNext.clicked.connect(self.nextButtonClicked)

        # pageTOC
        self.ui.checkBoxHasTOC.stateChanged.connect(lambda:self.hasTOCChanged(self.ui.checkBoxHasTOC))
        self.ui.scrollTOCPage.valueChanged.connect(self.tocPreviewChanged)
        self.ui.tocAddButton.clicked.connect(self.tocAddRowClicked)
        self.ui.buttonTOCPagePrev.clicked.connect(self.prevButtonClicked)
        self.ui.buttonTOCPageNext.clicked.connect(self.nextButtonClicked)

        # pageProcess
        self.ui.buttonProcessPrev.clicked.connect(self.prevButtonClicked)
        self.ui.buttonProcessNext.clicked.connect(self.nextButtonClicked)

        # pageSave
        self.ui.buttonSaveFile.clicked.connect(self.saveFileButtonClicked)

    def closeEvent(self, event):
        work_path = settings.value("path/work", os.path.join(gettempdir(), "ebook"))
        rmtree(work_path, ignore_errors=True)

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
        self.toc = {}

    def openFileDialog(self):
        load_path = settings.value("path/load", "C:\\")
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", load_path, "KOBO ePub (*.kepub.epub)")
        # Update settings
        load_path, self.file = os.path.split(path[0])
        if len(load_path):
            settings.setValue("path/load", load_path)

            work_path = settings.value("path/work", os.path.join(gettempdir(), "ebook"))
            self.book = eBook(path[0], work_path)
            self.book.load(self.loadProgressChanged, self.loadCompleted)

            self.ui.buttonSelectFile.setHidden(True)

    def nextButtonClicked(self):
        x = self.ui.stackedWidget.currentIndex()
        self.ui.stackedWidget.setCurrentIndex(x+1)

    def prevButtonClicked(self):
        x = self.ui.stackedWidget.currentIndex()
        self.ui.stackedWidget.setCurrentIndex(x-1)

    def showCurrentPage(self):
        currentPage = self.ui.stackedWidget.currentWidget().objectName()
        if currentPage == 'pageBegin':
            print("hello")
        elif currentPage == 'pageBookInfo':
            # update UI
            self.ui.tabButtonInfo.setEnabled(True)        
            self.ui.progressBarLoad.setHidden(True)
            self.ui.labelBookName.setHidden(False)            
            self.ui.labelBookName.setText(self.book.get_info("Title"))
            self.ui.labelPath.setText(os.path.join(settings.value("path/load"), self.file))
            self.ui.labelTitle.setText(self.book.get_info("Title"))
            self.ui.labelAuthor.setText(self.book.get_info("Author"))
            self.ui.labelPageCount.setText(self.book.get_info("PageCount"))
            self.ui.imageCover.setPixmap(QtGui.QPixmap(self.book.get_cover_page()))

            self.ui.buttonBeginNext.setEnabled(True)            
        elif currentPage == 'pageFirstPage':
            self.ui.tabButtonFirstPage.setEnabled(True)
            size = int(self.book.get_info("PageCount"))
            self.ui.scrollFirstPage.setMaximum(size)
            self.ui.scrollFirstPage.setValue(self.firstImage)
        elif currentPage == 'pageImageEnhance':
            self.ui.tabButtonImageEnhance.setEnabled(True)
            self.book.layout_fix(self.ui.scrollFirstPage.value())
            size = int(self.book.get_info("PageCount"))
            self.ui.scrollEnhancePage.setRange(1, size)
            self.ui.scrollEnhancePage.setValue(5)
        elif currentPage == 'pageTOC':
            self.ui.tabButtonTOC.setEnabled(True)
            size = int(self.book.get_info("PageCount"))
            self.ui.scrollTOCPage.setMaximum(size)
            self.ui.scrollTOCPage.setValue(self.tocPageNum)
            self.ui.checkBoxHasTOC.setChecked(True if self.tocPageNum > 0 else False)
        elif currentPage == 'pageProcess':
            self.ui.tabButtonProcess.setEnabled(True)
            # Pack TOC
            for i in range(self.ui.tocLineVerticalLayout.count()):
                # Skip the first row of header
                if i == 0:
                    continue
                if self.ui.tocLineVerticalLayout.itemAt(i).widget() is None:
                    continue
                key = self.ui.tocLineVerticalLayout.itemAt(i).widget().text()
                value = self.ui.tocPageVerticalLayout.itemAt(i).widget().text()
                if len(key) > 0 and len(value):
                    self.toc[key] = int(value)

            self.ui.progressBarSave.hide()
            self.book.save(self.firstImage, self.firstPageNum, self.tocPageNum, self.toc, self.ui.sliderContrast.value(), self.saveProgressChanged, self.saveCompleted)
        elif currentPage == 'pageSave':
            self.ui.tabButtonSaveFile.setEnabled(True)

    def loadProgressChanged(self, value):
        self.ui.progressBarLoad.show()
        self.ui.progressBarLoad.setValue(value)

    def loadCompleted(self):
        #self.book.parse()
        self.books.append(self.book)

        self.ui.stackedWidget.setCurrentWidget(self.ui.pageBookInfo)

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
        i = self.ui.scrollTOCPage.value()
        image = self.book.get_page(i)
        self.ui.imageTOCPage.setPixmap(QtGui.QPixmap(image))
        self.ui.labelTOCPage.setText(str(i))
        self.tocPageNum = i

    def tocAddRow(self, index):
        insert_at = 0
        for i in range(self.ui.tocButtonVerticalLayout.count()): 
            child = self.ui.tocButtonVerticalLayout.itemAt(i).widget() 
            if child is not None and "tocAddButton" == child.objectName():
                insert_at = i
                break

        # We start with a simple add button
        tocDelButton = QtWidgets.QPushButton(text="X")
        tocDelButton.setMaximumSize(QtCore.QSize(38, 38))
        tocDelButton.setMinimumSize(QtCore.QSize(38, 38))
        tocDelButton.setObjectName("tocDelButton_{}".format(index))
        tocDelButton.clicked.connect(lambda:self.tocDelRowClicked(tocDelButton))
        self.ui.tocButtonVerticalLayout.insertWidget(insert_at, tocDelButton)

        tocEditLine = QtWidgets.QLineEdit()
        tocEditLine.setObjectName("editTOCContent_{}".format(index))
        self.ui.tocLineVerticalLayout.insertWidget(insert_at, tocEditLine)

        tocEditPage = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(tocEditPage.sizePolicy().hasHeightForWidth())
        tocEditPage.setSizePolicy(sizePolicy)
        tocEditPage.setMaximumSize(QtCore.QSize(54, 16777215))
        tocEditPage.setMaxLength(3)
        tocEditPage.setObjectName("editTOCPage_{}".format(index))
        self.ui.tocPageVerticalLayout.insertWidget(insert_at, tocEditPage)

    def tocAddRowClicked(self):
        count = self.ui.tocButtonVerticalLayout.count()
        if count <= 3:
            index = 0
        else:
            # The 3rd last button is the last delete button.
            # label ... del ... add ... spacer
            button_name = self.ui.tocButtonVerticalLayout.itemAt(count-3).widget().objectName()
            index = int(button_name.replace("tocDelButton_", "")) + 1
        self.tocAddRow(index)

    def tocDelRowClicked(self, button):
        button_name = button.objectName()
        for i in range(self.ui.tocButtonVerticalLayout.count()): 
            if button_name == self.ui.tocButtonVerticalLayout.itemAt(i).widget().objectName():
                self.ui.tocButtonVerticalLayout.itemAt(i).widget().deleteLater()
                self.ui.tocLineVerticalLayout.itemAt(i).widget().deleteLater()
                self.ui.tocPageVerticalLayout.itemAt(i).widget().deleteLater()
                break

    def saveFileButtonClicked(self):        
        save_path = settings.value("path/save", os.path.expanduser("~/Documents"))
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", os.path.join(save_path, self.file), "KOBO ePub (*.kepub.epub)")
        if len(path):
            work_path = settings.value("path/work", os.path.join(gettempdir(), "ebook"))
            # Move output file from work folder for to save location.        
            move(os.path.join(work_path, self.file), path[0])
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