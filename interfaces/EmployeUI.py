
from os import path
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QWidget, QDialog)


class EmployeUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "employe.ui"), self)


