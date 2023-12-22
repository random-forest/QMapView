from PyQt5.QtGui import QPen, QColor, QPolygonF
from PyQt5.QtCore import QRectF

from .Item import Item


class LineItem(Item):

  def __init__(self, wgs84_points=[], r=1, color=QColor(), parent=None):
    super(LineItem, self).__init__(parent)
    self.wgs84_points = wgs84_points
    self.scene_points = []
    self.r = r
    self.rectf = None
    self.color = color

  def updatePos(self):
    self.scene_points = []

    for wgs84_point in self.wgs84_points:
      scene_point = self.scene().wgs84ToScene(wgs84_point)
      self.scene_points.append(scene_point)

    self.rectf = self.calc_rect()

  def calc_rect(self):
    if len(self.scene_points) == 0:
      return QRectF()
    return QPolygonF(self.scene_points).boundingRect()

  def boundingRect(self):
    return self.rectf

  def paint(self, painter=None, style=None, widget=None):
    if len(self.scene_points) > 0:
      painter.setPen(QPen(self.color, self.r))
      painter.drawPolyline(QPolygonF(self.scene_points))