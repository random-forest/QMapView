from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from src.core.View import View
from src.wigets.LayersListWidget import LayersListWidget
from src.wigets.CoordinatesWidget import CoordinatesWidget


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(0, 0, 1020, 840)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignRight)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.setMinimumWidth(1020)
        self.setMinimumHeight(840)

        self.mapView = View(self)

        self.layerWidget = LayersListWidget(self)
        self.coordsWidget = CoordinatesWidget(self.mapView)

        self.mainLayout.addWidget(self.mapView)
        # self.mainLayout.addWidget(self.coordsWidget)

        self.setLayout(self.mainLayout)
        self.show()

    def resizeEvent(self, event: QResizeEvent):
        self.mapView.resize(event.size())
        self.layerWidget.resize(self.layerWidget.width(), event.size().height())
        self.coordsWidget.updateGeometry()

