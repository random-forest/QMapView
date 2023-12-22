from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QByteArray

from config import Config
from src.TileSource import TileSource
from src.TileHttpLoader import TileHTTPLoader


class TileSourceHTTP(TileSource):
    remoteTileRequest = pyqtSignal(int, int, int)

    def __init__(self, name: str,  url: str, draw_options: dict, tile_size: int = Config.tileSize, scheme: str = Config.scheme, parent=None):
        super(TileSourceHTTP, self).__init__(parent)
        self.name = name

        self.tiles_url = url
        self.scheme = scheme
        self.draw_options = draw_options

        self._tile_size = tile_size
        self._min_zoom, self._max_zoom = Config.zoom[0], Config.zoom[1]

        self._tiles = dict()

        self._remote_loader = TileHTTPLoader()
        self._remote_loader.tileLoaded.connect(self.handleTileDataLoaded)

        self.remoteTileRequest.connect(self.remote_tile_request)

    def requestTile(self, x: int, y: int, zoom: int):
        self.remote_tile_request(x, y, zoom)

    def local_tile_loaded(self, x: int, y: int, zoom: int, pixmap: QPixmap):
        if not pixmap.isNull():
            self.tileReceived.emit(x, y, zoom, pixmap)

    def remote_tile_request(self, x: int, y: int, zoom: int):
        url = self.get_url(x, y, zoom)
        self._remote_loader.loadTile(x, y, zoom, url)

    def get_url(self, x: int, y: int, z: int) -> str:
        return self.tiles_url.format(z=z, x=x, y=y)

    def clear_tiles(self):
        self._tiles.clear()

    @pyqtSlot(int, int, int, QByteArray)
    def handleTileDataLoaded(self, x, y, zoom, data):
        pix = QPixmap()
        pix.loadFromData(data)

        self._tiles[(x, y)] = pix
        self.tileReceived.emit(x, y, zoom, pix)

    def abortAllRequests(self):
        self._remote_loader.abortAllRequests()

    @pyqtSlot()
    def close(self):
        self._remote_loader.abortAllRequests()
