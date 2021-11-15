from PyQt5.QtWidgets import QPushButton


class BigTile(QPushButton):
    def __init__(self, index_i, index_j):
        super(BigTile, self).__init__()

        self.setMaximumSize(42, 42)
        self.setEnabled(False)

        self.i = index_i
        self.j = index_j

    def get_position(self):
        return self.i, self.j
