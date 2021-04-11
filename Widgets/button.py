import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class TabButton(QtWidgets.QPushButton):
    """ Override QPushButton that have unique outlook and behavior """

    def __init__(self, parent=None):
        super().__init__(parent)