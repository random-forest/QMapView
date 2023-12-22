from PyQt5.QtCore import QObject, pyqtSignal, QPoint
from PyQt5.QtGui import QColor

from src import utils
from src.PointWGS84 import PointWGS84
from src.items.PointItem import PointItem

DEFAULT_CONFIG = {
    "default-location": {
        "lat": 47.073395,
        "lon": 31.526642
    },
    "cursor": {
        "default-radius": 8,
        "radius-values": [10, 12, 14, 16, 20, 24, 28],
        "color": [255, 255, 255, 255],
        "border-color": [0, 10, 20, 255]
    }
}


class Cursor(QObject):
    coordinatesUpdated = pyqtSignal(float, float)
    heightUpdated = pyqtSignal(int)

    def __init__(self, map_view, parent=None):
        super(Cursor, self).__init__(parent)

        self.map_view = map_view
        self.view_pos = None
        self.scene_pos = None
        self.wgs84_pos = None
        self.height = None
        self.marker = None

        self.config = DEFAULT_CONFIG

    def init_marker(self):
        self.wgs84_pos = PointWGS84(*DEFAULT_CONFIG["default-location"].values())

        color_rgba = self.config['cursor']['color']
        b_color_rgba = self.config['cursor']['border-color']

        color = QColor(color_rgba[0], color_rgba[1], color_rgba[2], color_rgba[3])
        border_color = QColor(b_color_rgba[0], b_color_rgba[1], b_color_rgba[2], b_color_rgba[3])

        self.marker = PointItem(self.wgs84_pos, self.config['cursor']['default-radius'])

        self.marker.setColor(color)
        self.marker.setBorderColor(border_color)
        self.map_view.scene().addItem(self.marker)
        # self.map_view.scene().zoomTo(self.marker.wgs84_pos, 12)
        self.update_marker()

    def update_marker(self):
        if not self.marker:
            self.init_marker()

        self.marker.setPos(self.wgs84_pos)
        self.coordinatesUpdated.emit(self.wgs84_pos.lat, self.wgs84_pos.lon)
        # self.update_height()

    def update_height(self):
        self.height = utils.get_altitude(
            self.wgs84_pos.lon, self.wgs84_pos.lat
        )
        self.heightUpdated.emit(self.height)

    def set_item_radius(self, r):
        self.marker.set_radius(r)
        self.update_marker()

    def zoomed(self):
        self.scene_pos = self.map_view.scene().wgs84_to_scene(self.wgs84_pos)
        self.update_marker()

    def set_view_pos(self, view_pos: QPoint):
        self.view_pos = view_pos

        self.scene_pos = self.map_view.mapToScene(view_pos)
        self.wgs84_pos = self.map_view.scene().sceneToWgs84(self.scene_pos)
        self.update_marker()

    def set_wgs84_pos(self, wgs84_pos: PointWGS84):
        self.wgs84_pos = wgs84_pos
        self.scene_pos = self.map_view.scene().wgs84ToScene(self.wgs84_pos)
        self.map_view.scene().setCenter(lat=wgs84_pos.lat, lon=wgs84_pos.lon)
        self.update_marker()

    def set_lat_lon(self, lat, lon):
        self.setWgs84Pos(PointWGS84(lat, lon))

    def center(self):
        if self.wgs84_pos:
            self.map_view.scene().set_center(lat=self.wgs84_pos.lat, lon=self.wgs84_pos.lon)
        else:
            self.set_wgs84_pos(PointWGS84(*self.config["default-location"].values()))
