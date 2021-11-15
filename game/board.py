from game.tiles.push_tile import PushTile
from game.tiles.tiny_tile import TinyTile
from game.tiles.big_tile import BigTile

from PyQt5.QtWidgets import QGridLayout


class Board:
    def __init__(self, size):
        self.size = size * 2 + 1
        self.board = [[0] * (self.size + 1) for i in range(self.size)]

        self.wrapper = QGridLayout()
        self.turn = 1

    def push_handler(self, tile: PushTile):
        tile.setStyleSheet('background:#000')

        tile.push(self.turn)
        self.turn += 1
        print(tile.turn_pushed)

        # check if left big tile is enclosed
        i, j = tile.i, tile.j

        if i > 0 or j > 0:
            if tile.is_vertical:
                if self.check_tile(i, j - 1) > 0:
                    self.board[i][j - 1].setStyleSheet("background: blue")

                if self.check_tile(i, j + 1) > 0:
                    self.board[i][j + 1].setStyleSheet("background: blue")
            else:
                if self.check_tile(i + 1, j) > 0:
                    self.board[i + 1][j].setStyleSheet("background: red")

                if self.check_tile(i - 1, j) > 0:
                    self.board[i - 1][j].setStyleSheet("background: red")

    def check_tile(self, i, j):
        tiles = [self.board[i][j - 1], self.board[i - 1][j], self.board[i][j + 1], self.board[i + 1][j]]

        tile: PushTile

        conclusion = -1

        for tile in tiles:
            if type(tile) == PushTile:
                if tile.turn_pushed == -1:
                    conclusion = -1
                    break

                if tile.turn_pushed > conclusion:
                    conclusion = tile.turn_pushed

        return conclusion

    def draw(self, wrapper):
        cutout_num = 0

        for i in range(self.size):
            if i < 11:
                if not i % 2:
                    cutout_num = i + 2

            if i >= 11:
                if i % 2:
                    cutout_num = i - 2 * abs(20 / 2 - i) + 1
            for j in range(self.size):
                tile = PushTile(i, j)

                if not i % 2:
                    if not j % 2:
                        tile = TinyTile()
                    else:
                        tile.make_horizontal()
                        tile.set_handler(self.push_handler)

                        self.board[i][j] = tile
                else:
                    if not j % 2:
                        tile.make_vertical()
                        tile.set_handler(self.push_handler)

                        self.board[i][j] = tile
                    else:
                        tile = BigTile(i, j)
                        self.board[i][j] = tile

                if abs((20 / 2) - j) - cutout_num >= 1:
                    self.board[i][j] = 1

                    tile.setVisible(False)

                wrapper.addWidget(tile, i, j)

    def __check_big_tile(self, i, j):
        self.board[i][j].setStyleSheet("background:black")
