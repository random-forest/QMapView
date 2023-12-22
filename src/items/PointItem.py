from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPen, QBrush, QColor

from src.items.Item import Item


class PointItem(Item):

  def __init__(self, wgs84_pos, r, color=QColor(), parent=None):
    super(PointItem, self).__init__(parent)
    self.wgs84_pos = wgs84_pos
    self.r = r
    self.scene_pos = None
    self.rectf = None
    self.pen = QPen(QColor())
    self.brush = QBrush(color)

  def updatePos(self):
    self.scene_pos = self.scene().wgs84ToScene(self.wgs84_pos)
    self.prepareGeometryChange()
    self.rectf = self.calcRect()

  def setRadius(self, r):
    self.r = r
    self.updatePos()

  def setPos(self, wgs84_pos):
    self.wgs84_pos = wgs84_pos
    self.updatePos()

  def calcRect(self):
    return QRectF(
      self.scene_pos.x() - self.r / 2,
      self.scene_pos.y() - self.r / 2,
      self.r,
      self.r
    )

  def boundingRect(self):
    return self.rectf

  def setColor(self, color):
    self.brush.setColor(color)

  def setBorderColor(self, color):
    self.pen.setColor(color)

  def paint(self, painter=None, style=None, widget=None):
    painter.setPen(self.pen)
    painter.setBrush(self.brush)

    painter.drawEllipse(self.boundingRect())

    if self.isSelected():
      painter.setPen(QPen(self.selection_color, self.selection_radius))
      painter.drawEllipse(self.boundingRect())
