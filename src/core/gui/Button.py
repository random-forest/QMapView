from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel

class Button(QFrame):
  def __init__(self, icon_path, parent = None):
    super(Button, self).__init__(parent)

    self.setStyleSheet("background-color: white;")
    self.setCursor(QCursor(Qt.PointingHandCursor))
    self.setMaximumWidth(20)
    self.setMaximumHeight(20)

    self.mainLayout = QHBoxLayout()
    self.mainLayout.setContentsMargins(0, 0, 0, 0)
    self.mainLayout.setSpacing(0)

    self.image = QPixmap(icon_path)
    self.imageLabel = QLabel()
    self.imageLabel.setPixmap(self.image)

    self.mainLayout.addWidget(self.imageLabel)

    self.setLayout(self.mainLayout)