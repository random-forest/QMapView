from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from src.core.gui.ButtonGroup import ButtonGroup


class ToolPanel(QFrame):
    def __init__(self, parent = None):
        super(ToolPanel, self).__init__(parent)
        self.setStyleSheet("background-color: #30363d; color: white;")
        self.setMaximumHeight(64)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.button_group = ButtonGroup()

        self.mainLayout.addWidget(self.button_group)

        self.setLayout(self.mainLayout)