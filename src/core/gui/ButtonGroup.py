from PyQt5.QtWidgets import QWidget, QGridLayout
from src.core.gui.Button import Button


class ButtonGroup(QWidget):
    def __init__(self, parent=None):
        super(ButtonGroup, self).__init__(parent)
        self.mainLayout = QGridLayout()

        self.layers_button = Button("static/layers.png")
        self.draw_button = Button("static/pencil.png")

        self.mainLayout.addWidget(self.layers_button)
        self.mainLayout.addWidget(self.draw_button)

        self.setLayout(self.mainLayout)