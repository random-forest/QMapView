import gpxpy
import codecs
import gpxpy.gpx

from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QResizeEvent, QPainter, QDropEvent, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QSizePolicy, QVBoxLayout, QPushButton

from src.Cursor import Cursor
from src.core.Scene import Scene

from src.PointWGS84 import PointWGS84
from src.items.PointItem import PointItem
from src.items.LineItem import LineItem

from src.core.gui.OverlayWidget import OverlayWidget
from src.utils import lonLatFromPos, get_elevation_from_rgb


class View(QGraphicsView):
    resized = pyqtSignal(QResizeEvent)
    fileDropped = pyqtSignal(QDropEvent)

    def __init__(self, parent=None):
        super(View, self).__init__(parent)

        self.setMinimumWidth(1020)
        self.setMinimumHeight(840)
        self.setMouseTracking(True)
        self.setScene(Scene(self))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setAcceptDrops(True)

        self.cursor = Cursor(map_view=self)
        self.cursor.init_marker()

        self.last_mouse_press_pos = None
        self.last_mouse_move_pos = None

        self.dragOver = False

        self.fileDropped.connect(self.drawDataSource)

        self.scene().zoomTo(self.cursor.wgs84_pos, 12)

    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setAccepted(True)
            self.dragOver = True
            self.update()

    def dropEvent(self, event):
        event.acceptProposedAction()
        self.fileDropped.emit(event)

    def resizeEvent(self, event):
        self.scene().setSize(event.size().width(), event.size().height())
        self.resized.emit(event)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.last_mouse_press_pos = event.pos()
            self.cursor.set_view_pos(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.last_mouse_press_pos = None

    def wheelEvent(self, event):
        super().wheelEvent(event)

        delta = event.angleDelta().y()

        if delta > 0:
            self.scene().zoomIn(self.cursor.wgs84_pos)
        else:
            self.scene().zoomOut(self.cursor.wgs84_pos)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        self.last_mouse_move_pos = event.pos()

        scene_pos = self.mapToScene(self.last_mouse_move_pos)
        wgs84_pos = self.scene().sceneToWgs84(scene_pos)

        self.parent().coordsWidget.lat.setData("lat: ", str(round(wgs84_pos.lat, 5)))
        self.parent().coordsWidget.lon.setData("lon: ", str(round(wgs84_pos.lon, 5)))

        if self.last_mouse_press_pos:
            delta = self.last_mouse_press_pos - event.pos()

            self.last_mouse_press_pos = event.pos()
            self.scene().translate(delta.x(), delta.y())

    def centerPos(self):
        return QPoint(self.rect().width() / 2, self.rect().height() / 2)

    def drawDataSource(self, event):
        file_path = event.mimeData().text()
        ext = file_path[file_path.index('.'):]

        if ext == ".gpx":
            self.processGPX(file_path[6:])
        elif ext == ".plt":
            self.processPLT(file_path[6:])

    def processGPX(self, file_path):
        gpx_file = open(file_path, 'r')
        gpx = gpxpy.parse(gpx_file)
        gpx_file.close()

        for track in gpx.tracks:
            for segment in track.segments:
                for i, point in enumerate(segment.points):
                    try:
                        if i == 0:
                            wgs_point = PointWGS84(point.latitude, point.longitude)
                            self.scene().zoomTo(wgs_point, 14)

                        p1 = PointWGS84(segment.points[i].latitude, segment.points[i].longitude)
                        p2 = PointWGS84(segment.points[i + 1].latitude, segment.points[i + 1].longitude)

                        self.scene().addItem(LineItem([p1, p2], 2, Qt.red))
                    except:
                        break

        for waypoint in gpx.waypoints:
            if waypoint.name == "VODA" or waypoint.name == "voda":
                wgs_pos = PointWGS84(waypoint.latitude, waypoint.longitude)
                marker = PointItem(wgs_pos, 8)
                marker.setColor(Qt.blue)
                self.scene().addItem(marker)

    @staticmethod
    def readPLT(file_path: str):
        arr = []
        with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as plt_file:
            for line in plt_file.readlines()[7:]:
                data = line.split(',')

                lat = float(data[0])
                lon = float(data[1].strip())

                arr.append(PointWGS84(lat, lon))
        return arr

    def processPLT(self, file_path):
        points = self.readPLT(file_path)

        for i, point in enumerate(points):
            try:
                if i == 0:
                    self.scene().zoomTo(points[i], 14)

                p1 = point
                p2 = points[i + 1]

                self.scene().addItem(LineItem([p1, p2], 2, Qt.darkYellow))
            except Exception as err:
                break

    @staticmethod
    def moveTo(x, y):
        return QPoint(x, y)
