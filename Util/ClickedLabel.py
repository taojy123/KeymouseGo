from PySide2.QtWidgets import QLabel
from PySide2 import QtWidgets
from PySide2.QtGui import QMouseEvent
from PySide2.QtCore import Signal, Qt


def test():
    print("clicked hbox layout test")


class Label(QLabel):

    clicked = Signal()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.clear()
        self.setText("clicked")



