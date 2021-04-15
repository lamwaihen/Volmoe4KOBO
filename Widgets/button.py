import sys
from PyQt5.QtWidgets import QPushButton

class TabButton(QPushButton):
    """ Override QPushButton that have unique outlook and behavior """

    def __init__(self, parent=None):
        super().__init__(parent)