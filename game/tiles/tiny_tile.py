from PyQt5.QtWidgets import QPushButton


class TinyTile(QPushButton):
    def __init__(self):
        super(TinyTile, self).__init__()

        self.setMaximumSize(8, 8)
        self.setEnabled(False)
