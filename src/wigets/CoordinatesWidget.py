from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QWidget


# x - lat, y - lon
class LabelGroup(QWidget):
    def __init__(self, label, value, parent=None):
        super(LabelGroup, self).__init__(parent)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.label = QLabel(label)
        self.value = QLabel(value)

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.value)

        self.setLayout(self.mainLayout)

    def setData(self, label, value):
        self.label.setText(label)
        self.value.setText(value)


class CoordinatesWidget(QFrame):
    def __init__(self, parent=None):
        super(CoordinatesWidget, self).__init__(parent)

        self.setStyleSheet("background-color: white; color: black; font-size: 16px;")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(0)

        self.lat = LabelGroup("lat: ", "0.0000")
        self.lon = LabelGroup("lon: ", "0.0000")

        self.setMinimumWidth(132)
        self.setMinimumHeight(42)

        self.mainLayout.addWidget(self.lat)
        self.mainLayout.addWidget(self.lon)

        self.setLayout(self.mainLayout)

    def updateGeometry(self):
        bottom_right = self.parent().geometry().bottomRight()
        self.setGeometry(bottom_right.x() - self.geometry().width(),
                         bottom_right.y() - self.geometry().height(),
                         self.geometry().width(), self.geometry().height())
