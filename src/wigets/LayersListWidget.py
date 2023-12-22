from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSlider
from config import Config

from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt


class FloatSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setOrientation(Qt.Horizontal)
        self.setRange(0, 100)
        self.setSingleStep(1)
        self.setPageStep(10)

    def value(self):
        return super().value() / 100.0


class ListItem(QFrame):
    def __init__(self, source, parent=None):
        super(ListItem, self).__init__(parent)
        self.source = source

        self.mainLayout = QVBoxLayout()

        self.nameLabel = QLabel(self.source.name)
        self.opacitySlider = FloatSlider(Qt.Orientation.Horizontal)
        self.opacitySlider.setValue(self.source.draw_options.get("opacity") * 100.0)
        self.opacitySlider.valueChanged.connect(self.setOpacity)

        self.mainLayout.addWidget(self.nameLabel)
        self.mainLayout.addWidget(self.opacitySlider)
        self.setLayout(self.mainLayout)

    def setOpacity(self, value):
        self.source.draw_options["opacity"] = self.opacitySlider.value()
        self.parent()._parent.mapView.scene().update()


class LayersListWidget(QFrame):
    def __init__(self, parent=None):
        super(LayersListWidget, self).__init__()

        self._parent = parent

        self.setStyleSheet("background-color: #30363d; color: white;")
        self.sources = self._parent.mapView.scene()._tile_sources

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)

        [self.mainLayout.addWidget(ListItem(s, parent=self)) for s in self.sources]

        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

        self.setLayout(self.mainLayout)
        self.show()

    def resizeEvent(self, event):
        self.resize(event.size())