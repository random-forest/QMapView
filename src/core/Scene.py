from numpy import floor
from typing import List
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QGraphicsScene, QWidget, QGraphicsProxyWidget
from PyQt5.QtCore import Qt, QSizeF, QRect, QRectF, QPointF, pyqtSignal

from src import utils
from config import Config
from src.PointWGS84 import PointWGS84
from src.TileSource.TileSourceHttp import TileSourceHTTP
from src.wigets.LayersListWidget import LayersListWidget


class Scene(QGraphicsScene):
    zoomChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)

        self._tile_sources = self.initTileSources()
        self._tile_sources = sorted(self._tile_sources, key=lambda s: s.draw_options.get("order"), reverse=True)

        self.empty_tile = QPixmap(Config.tileSize, Config.tileSize)
        self.empty_tile.fill(Qt.transparent)

        self.zoom = Config.zoom[0]
        self.tiles_rect = QRect()

        self.sceneRectChanged.connect(self.onSceneRectChanged)

    def initTileSources(self) -> List[TileSourceHTTP]:
        sources = []
        for source in Config.sources:
            tile_s = TileSourceHTTP(**source)
            tile_s.tileReceived.connect(self.setTilePixmap)
            sources.append(tile_s)
        return sources

    def centerPos(self) -> QPointF:
        return self.sceneRect().center()

    def setSize(self, width: float, height: float):
        self.setSceneRect(QRectF(self.sceneRect().topLeft(), QSizeF(width, height)))

    def translate(self, dx: float, dy: float):
        self.setSceneRect(self.sceneRect().translated(dx, dy))

    @staticmethod
    def tileFromPos(x: float, y: float) -> QPointF:
        tdim = float(Config.tileSize)
        return QPointF(x / tdim, y / tdim)

    @staticmethod
    def tileRect(tx: float, ty: float) -> QRectF:
        tdim = Config.tileSize
        return QRectF(tx * tdim, ty * tdim, tdim, tdim)

    def setTilePixmap(self, x, y, zoom, pixmap: QPixmap):
        """Set the image of the tile"""

        if self.zoom == zoom:
            self.update()

    def catchTileSource(self, x, y, zoom, pixmap):
        print(self.parent().last_mouse_move_pos)
        print(x, y, zoom, pixmap)

    def setCenter(self, lat: float, lon: float):
        x, y = self.posFromLatLon(lat, lon)
        self.setSceneCenter(x, y)

    def setSceneCenter(self, scene_x, scene_y):
        rect = QRectF(self.sceneRect())
        rect.moveCenter(QPointF(scene_x, scene_y))
        self.setSceneRect(rect)

    def posFromLatLon(self, lat, lon):
        return utils.posFromLonLat(lon, lat, self.zoom, Config.tileSize)

    def lonLatFromPos(self, x, y):
        return utils.lonLatFromPos(x, y, self.zoom, Config.tileSize)

    def wgs84ToScene(self, wgs84_pos):
        x, y = self.posFromLatLon(wgs84_pos.lat, wgs84_pos.lon)
        return QPointF(x, y)

    def sceneToWgs84(self, scene_pos):
        lon, lat = self.lonLatFromPos(scene_pos.x(), scene_pos.y())
        return PointWGS84(lat, lon)

    def onSceneRectChanged(self, rect):
        """Callback for the changing of the visible rect and request to load the new tiles"""
        tdim = Config.tileSize
        center = rect.center()
        ct = self.tileFromPos(center.x(), center.y())
        tx = ct.x()
        ty = ct.y()

        width = rect.width()
        height = rect.height()

        # top left corner of the center tile
        xp = int(width / 2.0 - (tx - floor(tx)) * tdim)
        yp = int(height / 2.0 - (ty - floor(ty)) * tdim)

        # first tile vertical and horizontal
        xs = tx - (xp + tdim - 1) / tdim
        ys = ty - (yp + tdim - 1) / tdim

        # last tile vertical and horizontal
        xe = (width - xp - 1) / tdim - xs + 1 + tx
        ye = (height - yp - 1) / tdim - ys + 1 + ty

        # define the rect of visible tiles
        self.tiles_rect = QRect(xs, ys, xe, ye)
        # Request the loading of new tiles (if needed)
        self.requestTiles()

    def requestTiles(self):
        """
        Request the loading of tiles.
        Check the loaded tiles and requests only the missing tiles
        """
        num_x_tiles = self.tiles_rect.width()
        num_y_tiles = self.tiles_rect.height()

        left = self.tiles_rect.left()
        top = self.tiles_rect.top()

        # Request load of new tiles
        for x in range(num_x_tiles):
            for y in range(num_y_tiles):
                tp = (left + x, top + y)

                for source in self._tile_sources:
                    if not source._tiles.get(tp):
                        source.requestTile(*tp, self.zoom)
                    else:
                        tile_pixmap = source._tiles.get(tp)
                        self.setTilePixmap(*tp, self.zoom, tile_pixmap)
                        if source.name == 'RGB Elevation':
                            self.catchTileSource(*tp, self.zoom, tile_pixmap)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        """
        Draw the background tiles.
        If a tile is not available, draw a rectangle
        """
        left = self.tiles_rect.left()
        top = self.tiles_rect.top()

        num_xtiles = self.tiles_rect.width()
        num_ytiles = self.tiles_rect.height()

        tdim = Config.tileSize
        pix_rect = QRectF(0.0, 0.0, tdim, tdim)

        painter.setClipRect(rect)

        for x in range(num_xtiles + 1):
            for y in range(num_ytiles + 1):
                tp = (x + left, y + top)
                box = self.tileRect(*tp)

                for source in self._tile_sources:
                    tiles = source._tiles

                    tile = tiles.get(tp, self.empty_tile)
                    opacity = source.draw_options.get("opacity")
                    painter.setOpacity(opacity)
                    painter.drawPixmap(box, tile, pix_rect)

    def zoomIn(self, pos):
        self.zoomTo(pos, self.zoom + 1)

    def zoomOut(self, pos):
        self.zoomTo(pos, self.zoom - 1)

    def zoomTo(self, pos, zoom):
        if zoom > Config.zoom[1] or zoom < Config.zoom[0]:
            return

        self.zoom = zoom

        for source in self._tile_sources:
            source.abortAllRequests()
            # source.clear_tiles()

        self.setCenter(lat=pos.lat, lon=pos.lon)

        self.zoomChanged.emit(zoom)
