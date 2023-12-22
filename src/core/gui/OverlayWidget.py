from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from src.wigets.CoordinatesWidget import CoordinatesWidget


class OverlayWidget(QWidget):
    resized = pyqtSignal(QResizeEvent)

    def __init__(self, parent=None):
        super(OverlayWidget, self).__init__(parent)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setMinimumWidth(1024)
        self.setMinimumHeight(840)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(0)

        self.mainLayout.addWidget(CoordinatesWidget(self))

        self.setLayout(self.mainLayout)
        self.show()

    def resizeEvent(self, event):
        self.resize(event.size())