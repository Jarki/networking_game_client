from forms.basic_form import BasicForm
from game.board import Board


from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QLayout
from PyQt5.QtWidgets import QWidget, QLabel, QLayout

from PyQt5.QtCore import Qt


class Game(BasicForm):
    def __init__(self, container_layout: QLayout, container_widget: QWidget):
        super().__init__()

        self.container = QHBoxLayout()

        self.board_wrapper = QGridLayout()
        self.board_wrapper.setSpacing(0)
        self.board_wrapper.setAlignment(Qt.AlignmentFlag.AlignAbsolute)

        self.game_info = QVBoxLayout()
        self.active_player_label = QLabel('Current player')
        self.turn_number_label = QLabel('Turn #')

        self.game_info.addWidget(self.active_player_label)
        self.game_info.addWidget(self.turn_number_label)
        self.game_info.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.game_info.setContentsMargins(0, 0, 20, 0)

        self.container.addLayout(self.board_wrapper)
        self.container.addLayout(self.game_info)

        container_layout.addLayout(self.container)

        self.opponent = ""

        # setup game board
        self.board = None
        self.setup_board()

    def setup_board(self):
        self.board = Board(10)
        self.board.draw(self.board_wrapper)

        self.board.set_event_handler("active_player_toggled", self.on_player_toggle)
        self.board.set_event_handler("new_turn", self.on_new_turn)

    def on_player_toggle(self, b: Board):
        if b.active_player:
            self.active_player_label.setText('Your turn')
        else:
            self.active_player_label.setText(f'{self.opponent}s\' turn')

    def on_new_turn(self, b: Board):
        self.turn_number_label.setText(f'Turn #{b.turn}')

    def update(self, pos: tuple):
        self.board.push(pos)

