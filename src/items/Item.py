from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsItem

class Item(QGraphicsItem):

  def __init__(self, parent=None):
    super(Item, self).__init__(parent)
    self.setFlag(self.ItemIsSelectable)
    self.selection_color = QColor(0, 255, 0)
    self.selection_radius = 2
    self.valid = True

  def itemChange(self, change, value):
    if change == self.ItemSceneChange:
      old_scene = self.scene()
      new_scene = value

      if old_scene is not None:
        old_scene.zoomChanged.disconnect(self.setZoom)
      if new_scene is not None:
        new_scene.zoomChanged.connect(self.setZoom)

    elif change == self.ItemSceneHasChanged:
      scene = value
      if scene is not None:
        self.updatePos()

    return value

  def center(self):
    if self.scene():
      center = self.boundingRect().center()
      self.scene().set_scene_center(center.x(), center.y())

  def setZoom(self, zoom):
    self.updatePos()

  def updatePos(self):
    raise NotImplementedError()
