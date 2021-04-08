# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'm:\Documents\GitHub\Volmoe4KOBO\UI\Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        MainWindow.setFont(font)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setAutoFillBackground(False)
        self.toolBox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox.setObjectName("toolBox")
        self.tabBegin = QtWidgets.QWidget()
        self.tabBegin.setGeometry(QtCore.QRect(0, 0, 69, 375))
        self.tabBegin.setObjectName("tabBegin")
        self.label_2 = QtWidgets.QLabel(self.tabBegin)
        self.label_2.setGeometry(QtCore.QRect(9, 9, 23, 16))
        self.label_2.setObjectName("label_2")
        self.toolBox.addItem(self.tabBegin, "")
        self.tabFirstPage = QtWidgets.QWidget()
        self.tabFirstPage.setGeometry(QtCore.QRect(0, 0, 69, 375))
        self.tabFirstPage.setObjectName("tabFirstPage")
        self.toolBox.addItem(self.tabFirstPage, "")
        self.tabImageEnhance = QtWidgets.QWidget()
        self.tabImageEnhance.setGeometry(QtCore.QRect(0, 0, 69, 375))
        self.tabImageEnhance.setObjectName("tabImageEnhance")
        self.toolBox.addItem(self.tabImageEnhance, "")
        self.tabTOC = QtWidgets.QWidget()
        self.tabTOC.setGeometry(QtCore.QRect(0, 0, 69, 375))
        self.tabTOC.setObjectName("tabTOC")
        self.toolBox.addItem(self.tabTOC, "")
        self.tabProcess = QtWidgets.QWidget()
        self.tabProcess.setGeometry(QtCore.QRect(0, 0, 69, 375))
        self.tabProcess.setObjectName("tabProcess")
        self.toolBox.addItem(self.tabProcess, "")
        self.tabUpload = QtWidgets.QWidget()
        self.tabUpload.setGeometry(QtCore.QRect(0, 0, 69, 375))
        self.tabUpload.setObjectName("tabUpload")
        self.toolBox.addItem(self.tabUpload, "")
        self.horizontalLayout.addWidget(self.toolBox)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(707, 543))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.pageBegin = QtWidgets.QWidget()
        self.pageBegin.setObjectName("pageBegin")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.pageBegin)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.pageBegin)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.progressBarLoad = QtWidgets.QProgressBar(self.pageBegin)
        self.progressBarLoad.setAutoFillBackground(False)
        self.progressBarLoad.setProperty("value", 0)
        self.progressBarLoad.setTextVisible(True)
        self.progressBarLoad.setInvertedAppearance(False)
        self.progressBarLoad.setObjectName("progressBarLoad")
        self.gridLayout.addWidget(self.progressBarLoad, 0, 1, 1, 1)
        self.buttonSelectFile = QtWidgets.QPushButton(self.pageBegin)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSelectFile.sizePolicy().hasHeightForWidth())
        self.buttonSelectFile.setSizePolicy(sizePolicy)
        self.buttonSelectFile.setObjectName("buttonSelectFile")
        self.gridLayout.addWidget(self.buttonSelectFile, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.gridLayout_1.setObjectName("gridLayout_1")
        self.imageCover = ImageWidget(self.pageBegin)
        self.imageCover.setFrameShape(QtWidgets.QFrame.Panel)
        self.imageCover.setFrameShadow(QtWidgets.QFrame.Plain)
        self.imageCover.setLineWidth(1)
        self.imageCover.setMidLineWidth(0)
        self.imageCover.setText("")
        self.imageCover.setAlignment(QtCore.Qt.AlignCenter)
        self.imageCover.setObjectName("imageCover")
        self.gridLayout_1.addWidget(self.imageCover, 0, 2, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label_7 = QtWidgets.QLabel(self.pageBegin)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtWidgets.QLabel(self.pageBegin)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtWidgets.QLabel(self.pageBegin)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.labelPath = QtWidgets.QLabel(self.pageBegin)
        self.labelPath.setText("")
        self.labelPath.setObjectName("labelPath")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.labelPath)
        self.labelTitle = QtWidgets.QLabel(self.pageBegin)
        self.labelTitle.setText("")
        self.labelTitle.setObjectName("labelTitle")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.labelTitle)
        self.labelAuthor = QtWidgets.QLabel(self.pageBegin)
        self.labelAuthor.setText("")
        self.labelAuthor.setObjectName("labelAuthor")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.labelAuthor)
        self.label_10 = QtWidgets.QLabel(self.pageBegin)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.labelPageCount = QtWidgets.QLabel(self.pageBegin)
        self.labelPageCount.setText("")
        self.labelPageCount.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelPageCount.setObjectName("labelPageCount")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.labelPageCount)
        self.gridLayout_1.addLayout(self.formLayout, 0, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_1)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_1.addItem(spacerItem1)
        self.buttonBeginNext = QtWidgets.QPushButton(self.pageBegin)
        self.buttonBeginNext.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBeginNext.sizePolicy().hasHeightForWidth())
        self.buttonBeginNext.setSizePolicy(sizePolicy)
        self.buttonBeginNext.setObjectName("buttonBeginNext")
        self.horizontalLayout_1.addWidget(self.buttonBeginNext)
        self.verticalLayout_4.addLayout(self.horizontalLayout_1)
        self.verticalLayout_4.setStretch(2, 1)
        self.stackedWidget.addWidget(self.pageBegin)
        self.pageFirstPage = QtWidgets.QWidget()
        self.pageFirstPage.setObjectName("pageFirstPage")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.pageFirstPage)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.pageFirstPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_6.addWidget(self.label_5)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_14 = QtWidgets.QLabel(self.pageFirstPage)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.spinFirstPage = QtWidgets.QSpinBox(self.pageFirstPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinFirstPage.sizePolicy().hasHeightForWidth())
        self.spinFirstPage.setSizePolicy(sizePolicy)
        self.spinFirstPage.setReadOnly(False)
        self.spinFirstPage.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinFirstPage.setProperty("value", 1)
        self.spinFirstPage.setObjectName("spinFirstPage")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinFirstPage)
        self.verticalLayout_6.addLayout(self.formLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.imageFirstPage = ImageWidget(self.pageFirstPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageFirstPage.sizePolicy().hasHeightForWidth())
        self.imageFirstPage.setSizePolicy(sizePolicy)
        self.imageFirstPage.setMinimumSize(QtCore.QSize(311, 471))
        self.imageFirstPage.setFrameShape(QtWidgets.QFrame.Box)
        self.imageFirstPage.setText("")
        self.imageFirstPage.setAlignment(QtCore.Qt.AlignCenter)
        self.imageFirstPage.setObjectName("imageFirstPage")
        self.gridLayout_2.addWidget(self.imageFirstPage, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.pageFirstPage)
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 1, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_12 = QtWidgets.QLabel(self.pageFirstPage)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_6.addWidget(self.label_12)
        self.labelFirstPage = QtWidgets.QLabel(self.pageFirstPage)
        self.labelFirstPage.setText("")
        self.labelFirstPage.setObjectName("labelFirstPage")
        self.horizontalLayout_6.addWidget(self.labelFirstPage)
        self.scrollFirstPage = QtWidgets.QScrollBar(self.pageFirstPage)
        self.scrollFirstPage.setOrientation(QtCore.Qt.Horizontal)
        self.scrollFirstPage.setObjectName("scrollFirstPage")
        self.horizontalLayout_6.addWidget(self.scrollFirstPage)
        self.horizontalLayout_6.setStretch(2, 1)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.buttonFirstPageNext = QtWidgets.QPushButton(self.pageFirstPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonFirstPageNext.sizePolicy().hasHeightForWidth())
        self.buttonFirstPageNext.setSizePolicy(sizePolicy)
        self.buttonFirstPageNext.setObjectName("buttonFirstPageNext")
        self.horizontalLayout_3.addWidget(self.buttonFirstPageNext)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6.setStretch(2, 1)
        self.stackedWidget.addWidget(self.pageFirstPage)
        self.pageImageEnhance = QtWidgets.QWidget()
        self.pageImageEnhance.setObjectName("pageImageEnhance")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.pageImageEnhance)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.pageImageEnhance)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_11 = QtWidgets.QLabel(self.pageImageEnhance)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.labelContrast = QtWidgets.QLabel(self.pageImageEnhance)
        self.labelContrast.setText("")
        self.labelContrast.setObjectName("labelContrast")
        self.horizontalLayout_4.addWidget(self.labelContrast)
        self.sliderContrast = QtWidgets.QSlider(self.pageImageEnhance)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sliderContrast.sizePolicy().hasHeightForWidth())
        self.sliderContrast.setSizePolicy(sizePolicy)
        self.sliderContrast.setMaximum(128)
        self.sliderContrast.setSingleStep(4)
        self.sliderContrast.setPageStep(16)
        self.sliderContrast.setProperty("value", 32)
        self.sliderContrast.setSliderPosition(32)
        self.sliderContrast.setOrientation(QtCore.Qt.Horizontal)
        self.sliderContrast.setInvertedAppearance(False)
        self.sliderContrast.setInvertedControls(False)
        self.sliderContrast.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderContrast.setTickInterval(8)
        self.sliderContrast.setObjectName("sliderContrast")
        self.horizontalLayout_4.addWidget(self.sliderContrast)
        self.horizontalLayout_4.setStretch(2, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)
        self.imageEnhanceRight = ImageWidget(self.pageImageEnhance)
        self.imageEnhanceRight.setFrameShape(QtWidgets.QFrame.Panel)
        self.imageEnhanceRight.setFrameShadow(QtWidgets.QFrame.Plain)
        self.imageEnhanceRight.setLineWidth(1)
        self.imageEnhanceRight.setMidLineWidth(0)
        self.imageEnhanceRight.setText("")
        self.imageEnhanceRight.setAlignment(QtCore.Qt.AlignCenter)
        self.imageEnhanceRight.setObjectName("imageEnhanceRight")
        self.gridLayout_3.addWidget(self.imageEnhanceRight, 0, 1, 1, 1)
        self.imageEnhanceLeft = ImageWidget(self.pageImageEnhance)
        self.imageEnhanceLeft.setFrameShape(QtWidgets.QFrame.Panel)
        self.imageEnhanceLeft.setText("")
        self.imageEnhanceLeft.setAlignment(QtCore.Qt.AlignCenter)
        self.imageEnhanceLeft.setObjectName("imageEnhanceLeft")
        self.gridLayout_3.addWidget(self.imageEnhanceLeft, 0, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_13 = QtWidgets.QLabel(self.pageImageEnhance)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_8.addWidget(self.label_13)
        self.labelEnhancePage = QtWidgets.QLabel(self.pageImageEnhance)
        self.labelEnhancePage.setText("")
        self.labelEnhancePage.setObjectName("labelEnhancePage")
        self.horizontalLayout_8.addWidget(self.labelEnhancePage)
        self.scrollEnhancePage = QtWidgets.QScrollBar(self.pageImageEnhance)
        self.scrollEnhancePage.setOrientation(QtCore.Qt.Horizontal)
        self.scrollEnhancePage.setObjectName("scrollEnhancePage")
        self.horizontalLayout_8.addWidget(self.scrollEnhancePage)
        self.horizontalLayout_8.setStretch(2, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.gridLayout_3.setRowStretch(0, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.buttonEnhancePageNext = QtWidgets.QPushButton(self.pageImageEnhance)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonEnhancePageNext.sizePolicy().hasHeightForWidth())
        self.buttonEnhancePageNext.setSizePolicy(sizePolicy)
        self.buttonEnhancePageNext.setObjectName("buttonEnhancePageNext")
        self.horizontalLayout_2.addWidget(self.buttonEnhancePageNext)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(1, 1)
        self.stackedWidget.addWidget(self.pageImageEnhance)
        self.pageTOC = QtWidgets.QWidget()
        self.pageTOC.setObjectName("pageTOC")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pageTOC)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_1 = QtWidgets.QLabel(self.pageTOC)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setObjectName("label_1")
        self.verticalLayout_3.addWidget(self.label_1)
        self.checkBoxHasTOC = QtWidgets.QCheckBox(self.pageTOC)
        self.checkBoxHasTOC.setChecked(True)
        self.checkBoxHasTOC.setObjectName("checkBoxHasTOC")
        self.verticalLayout_3.addWidget(self.checkBoxHasTOC)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_61 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_61.setObjectName("horizontalLayout_61")
        self.labelTOCPage = QtWidgets.QLabel(self.pageTOC)
        self.labelTOCPage.setText("")
        self.labelTOCPage.setObjectName("labelTOCPage")
        self.horizontalLayout_61.addWidget(self.labelTOCPage)
        self.label_3 = QtWidgets.QLabel(self.pageTOC)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_61.addWidget(self.label_3)
        self.scrollTOCPage = QtWidgets.QScrollBar(self.pageTOC)
        self.scrollTOCPage.setOrientation(QtCore.Qt.Horizontal)
        self.scrollTOCPage.setObjectName("scrollTOCPage")
        self.horizontalLayout_61.addWidget(self.scrollTOCPage)
        self.horizontalLayout_61.setStretch(2, 1)
        self.gridLayout_4.addLayout(self.horizontalLayout_61, 2, 0, 1, 1)
        self.imageTOCPage = ImageWidget(self.pageTOC)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageTOCPage.sizePolicy().hasHeightForWidth())
        self.imageTOCPage.setSizePolicy(sizePolicy)
        self.imageTOCPage.setMinimumSize(QtCore.QSize(311, 471))
        self.imageTOCPage.setFrameShape(QtWidgets.QFrame.Box)
        self.imageTOCPage.setText("")
        self.imageTOCPage.setAlignment(QtCore.Qt.AlignCenter)
        self.imageTOCPage.setObjectName("imageTOCPage")
        self.gridLayout_4.addWidget(self.imageTOCPage, 0, 0, 1, 1)
        self.tocHorizontalLayout = QtWidgets.QHBoxLayout()
        self.tocHorizontalLayout.setObjectName("tocHorizontalLayout")
        self.tocButtonVerticalLayout = QtWidgets.QVBoxLayout()
        self.tocButtonVerticalLayout.setContentsMargins(0, -1, -1, -1)
        self.tocButtonVerticalLayout.setObjectName("tocButtonVerticalLayout")
        self.tocAddButton = QtWidgets.QPushButton(self.pageTOC)
        self.tocAddButton.setMaximumSize(QtCore.QSize(21, 21))
        self.tocAddButton.setObjectName("tocAddButton")
        self.tocButtonVerticalLayout.addWidget(self.tocAddButton)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tocButtonVerticalLayout.addItem(spacerItem4)
        self.tocHorizontalLayout.addLayout(self.tocButtonVerticalLayout)
        self.tocLineVerticalLayout = QtWidgets.QVBoxLayout()
        self.tocLineVerticalLayout.setContentsMargins(0, -1, -1, -1)
        self.tocLineVerticalLayout.setSpacing(6)
        self.tocLineVerticalLayout.setObjectName("tocLineVerticalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tocLineVerticalLayout.addItem(spacerItem5)
        self.tocHorizontalLayout.addLayout(self.tocLineVerticalLayout)
        self.tocPageVerticalLayout = QtWidgets.QVBoxLayout()
        self.tocPageVerticalLayout.setContentsMargins(0, -1, -1, -1)
        self.tocPageVerticalLayout.setObjectName("tocPageVerticalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tocPageVerticalLayout.addItem(spacerItem6)
        self.tocHorizontalLayout.addLayout(self.tocPageVerticalLayout)
        self.gridLayout_4.addLayout(self.tocHorizontalLayout, 0, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.buttonTOCPageNext = QtWidgets.QPushButton(self.pageTOC)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonTOCPageNext.sizePolicy().hasHeightForWidth())
        self.buttonTOCPageNext.setSizePolicy(sizePolicy)
        self.buttonTOCPageNext.setObjectName("buttonTOCPageNext")
        self.horizontalLayout_7.addWidget(self.buttonTOCPageNext)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.setStretch(2, 1)
        self.stackedWidget.addWidget(self.pageTOC)
        self.pageProcess = QtWidgets.QWidget()
        self.pageProcess.setObjectName("pageProcess")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.pageProcess)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_31 = QtWidgets.QLabel(self.pageProcess)
        self.label_31.setObjectName("label_31")
        self.verticalLayout_5.addWidget(self.label_31)
        self.progressBarSave = QtWidgets.QProgressBar(self.pageProcess)
        self.progressBarSave.setProperty("value", 24)
        self.progressBarSave.setObjectName("progressBarSave")
        self.verticalLayout_5.addWidget(self.progressBarSave)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        self.buttonProcessNext = QtWidgets.QPushButton(self.pageProcess)
        self.buttonProcessNext.setEnabled(False)
        self.buttonProcessNext.setObjectName("buttonProcessNext")
        self.horizontalLayout_5.addWidget(self.buttonProcessNext)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayout_5.setStretch(1, 1)
        self.stackedWidget.addWidget(self.pageProcess)
        self.pageSave = QtWidgets.QWidget()
        self.pageSave.setObjectName("pageSave")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.pageSave)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_15 = QtWidgets.QLabel(self.pageSave)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_14.addWidget(self.label_15)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.buttonSaveFile = QtWidgets.QPushButton(self.pageSave)
        self.buttonSaveFile.setObjectName("buttonSaveFile")
        self.gridLayout_5.addWidget(self.buttonSaveFile, 0, 0, 1, 1)
        self.verticalLayout_14.addLayout(self.gridLayout_5)
        self.stackedWidget.addWidget(self.pageSave)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(False)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(4)
        self.toolBox.currentChanged['int'].connect(self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Volmoe4KOBO"))
        self.label_2.setText(_translate("MainWindow", "Intro"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.tabBegin), _translate("MainWindow", "Begin"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.tabFirstPage), _translate("MainWindow", "設定首頁"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.tabImageEnhance), _translate("MainWindow", "畫面優化"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.tabTOC), _translate("MainWindow", "目錄編輯"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.tabProcess), _translate("MainWindow", "內容處理"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.tabUpload), _translate("MainWindow", "上傳檔案"))
        self.label.setText(_translate("MainWindow", "選取一個或多個ePub檔案開始調整。"))
        self.buttonSelectFile.setText(_translate("MainWindow", "選取檔案…"))
        self.label_7.setText(_translate("MainWindow", "檔案："))
        self.label_8.setText(_translate("MainWindow", "書名："))
        self.label_9.setText(_translate("MainWindow", "作者："))
        self.label_10.setText(_translate("MainWindow", "頁數："))
        self.buttonBeginNext.setText(_translate("MainWindow", "下一步"))
        self.label_5.setText(_translate("MainWindow", "選取書本打開後的第一頁。如果從缺，請選擇第一張頁面並設定其頁碼。"))
        self.label_14.setText(_translate("MainWindow", "頁碼："))
        self.spinFirstPage.setSuffix(_translate("MainWindow", "頁"))
        self.spinFirstPage.setPrefix(_translate("MainWindow", "第"))
        self.label_12.setText(_translate("MainWindow", "選取頁面："))
        self.buttonFirstPageNext.setText(_translate("MainWindow", "下一步"))
        self.label_4.setText(_translate("MainWindow", "調整畫面對比度。"))
        self.label_11.setText(_translate("MainWindow", "對比度："))
        self.label_13.setText(_translate("MainWindow", "選取頁面："))
        self.buttonEnhancePageNext.setText(_translate("MainWindow", "下一步"))
        self.label_1.setText(_translate("MainWindow", "選取目錄所在頁面。"))
        self.checkBoxHasTOC.setText(_translate("MainWindow", "有目錄頁"))
        self.checkBoxHasTOC.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.label_3.setText(_translate("MainWindow", "頁碼："))
        self.tocAddButton.setText(_translate("MainWindow", "+"))
        self.buttonTOCPageNext.setText(_translate("MainWindow", "下一步"))
        self.label_31.setText(_translate("MainWindow", "檔案分析中，請稍候。"))
        self.buttonProcessNext.setText(_translate("MainWindow", "下一步"))
        self.label_15.setText(_translate("MainWindow", "請選擇儲存檔案的方式。"))
        self.buttonSaveFile.setText(_translate("MainWindow", "儲存檔案"))
from Widgets.label import ImageWidget
