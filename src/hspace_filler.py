from PyQt5.QtWidgets import QWidget, QSizePolicy


class HSpaceFiller(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)