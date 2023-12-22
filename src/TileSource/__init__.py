from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QObject


class TileSource(QObject):
    tileReceived = pyqtSignal(int, int, int, QPixmap)

    def __init__(self, parent=None):
        super(TileSource, self).__init__(parent)

        self._tile_size = None
        self._min_zoom = None
        self._max_zoom = None

    def tileSize(self):
        return self._tile_size

    def minZoom(self):
        return self._min_zoom

    def maxZoom(self):
        return self._max_zoom