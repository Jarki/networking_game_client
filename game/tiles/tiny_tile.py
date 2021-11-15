from game.tiles.constraints import Constraints

from PyQt5.QtWidgets import QPushButton


class TinyTile(QPushButton):
    def __init__(self):
        super(TinyTile, self).__init__()

        self.setMaximumSize(Constraints.smaller_distance, Constraints.smaller_distance)
        self.setEnabled(False)
