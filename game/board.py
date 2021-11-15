import logging

from game.tiles.push_tile import PushTile
from game.tiles.tiny_tile import TinyTile
from game.tiles.big_tile import BigTile


class Board:
    def __init__(self, size, is_first_turn=True):
        self.size = size * 2 + 1
        self.board: list[list[PushTile]] = [[PushTile(0, 0)] * self.size for i in range(self.size)]

        self.turn = 1

        self.event_handlers = {
            "active_player_toggled": lambda x: x,
            "new_turn": lambda x: x
        }

        self.active_player = not is_first_turn
        self.toggle_active_player()

    def toggle_active_player(self):
        self.active_player = not self.active_player

        self.event_handlers["active_player_toggled"](self)

    def new_turn(self, tile):
        tile.push(self.turn)
        self.turn += 1

        self.event_handlers["new_turn"](self)

    def set_event_handler(self, event_name, callback):
        logging.debug(f'set a handler for event {event_name}')

        if event_name in self.event_handlers:
            self.event_handlers[event_name] = callback

    def __is_in_bounds(self, indexes: tuple):
        if (indexes[0] > 0 and indexes[1] > 0) and (indexes[1] < self.size and indexes[0] < self.size):
            return True

        return False

    def push_handler(self, tile: PushTile):
        tile.setStyleSheet('background:#000')

        self.new_turn(tile)

        # check if left big tile is enclosed
        i, j = tile.i, tile.j
        self.toggle_active_player()
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
        if not self.__is_in_bounds((i, j)):
            return -1

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
            else:
                conclusion = -1
                break

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
                    tile.setVisible(False)

                wrapper.addWidget(tile, i, j)

    def __check_big_tile(self, i: int, j: int):
        self.board[i][j].setStyleSheet("background:black")

    def push(self, pos: tuple[int, int]):
        tile: PushTile = self.board[pos[0]][pos[1]]

        self.push_handler(tile)
