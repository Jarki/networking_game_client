from game.tiles.constraints import Constraints

from PyQt5.QtWidgets import QPushButton


class PushTile(QPushButton):
    def __init__(self, index_i, index_j, is_vertical = False):
        super(PushTile, self).__init__()

        self.i = index_i
        self.j = index_j

        self.is_vertical = is_vertical
        self.turn_pushed = -1

        if is_vertical:
            self.make_vertical()
        else:
            self.make_horizontal()

        self.handler = lambda x: x
        self.clicked.connect(self.__call_handler)

    def make_vertical(self):
        self.is_vertical = True
        self.setMaximumSize(Constraints.smaller_distance, Constraints.bigger_distance)

    def make_horizontal(self):
        self.is_vertical = False
        self.setMaximumSize(Constraints.bigger_distance, Constraints.smaller_distance)

    def push(self, turn_number):
        self.turn_pushed = turn_number

    def __call_handler(self):
        self.handler(self)

    def set_handler(self, handler):
        self.handler = handler








