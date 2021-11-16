from forms.basic_form import BasicForm
from game.board import Board

import logging

from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QLayout
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget

from PyQt5.QtCore import Qt


class Game(BasicForm):
    def __init__(self, container_layout: QLayout, container_widget: QWidget):
        super().__init__()

        self.container = QHBoxLayout()

        self.board_wrapper = QGridLayout()
        self.board_wrapper.setSpacing(0)
        self.board_wrapper.setAlignment(Qt.AlignmentFlag.AlignAbsolute)

        self.game_info_wrapper = QVBoxLayout()
        self.game_info = QVBoxLayout()

        self.game_chat = QListWidget()
        self.game_chat.setMaximumWidth(200)

        self.active_player_label = QLabel('Current player')
        self.turn_number_label = QLabel('Turn #')
        self.player1_points_label = QLabel('Your points: 0')
        self.player2_points_label = QLabel(f'Your opponents\' points: 0')

        self.game_info.addWidget(self.active_player_label)
        self.game_info.addWidget(self.turn_number_label)
        self.game_info.addWidget(self.player1_points_label)
        self.game_info.addWidget(self.player2_points_label)
        self.game_info.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.game_info.setContentsMargins(0, 0, 50, 20)

        self.game_info_wrapper.addLayout(self.game_info)
        self.game_info_wrapper.addWidget(self.game_chat)

        self.container.addLayout(self.board_wrapper)
        self.container.addLayout(self.game_info_wrapper)

        container_layout.addLayout(self.container)

        self.event_handlers = {
            "update": lambda x: x
        }

        # setup game board
        self.opponent = ""
        self.board = None

    def set_opponent(self, name):
        self.opponent = name

    def setup_board(self, has_first_turn=True):
        self.board = Board(10, has_first_turn)
        self.board.draw(self.board_wrapper)

        self.board.set_event_handler("button_pressed", self.on_push)
        self.board.set_event_handler("active_player_toggled", self.on_player_toggle)
        self.board.set_event_handler("new_turn", self.on_new_turn)
        self.board.set_event_handler("point", self.on_point_update)

    def set_event_handler(self, event_name, callback):
        if event_name in self.event_handlers:
            logging.debug(f'set a handler for event {event_name}')
            self.event_handlers[event_name] = callback

    def on_push(self, pos: tuple):
        """This function raises an "event" and update when a button on the board is pushed"""
        self.event_handlers["update"](pos)

    def on_player_toggle(self, b: Board):
        """This function sets correct text for the labels"""
        if b.active_player:
            self.active_player_label.setText('Your turn')
        else:
            self.active_player_label.setText(f'{self.opponent}s\' turn')

    def on_new_turn(self, b: Board):
        """This function sets correct text for the labels"""
        self.turn_number_label.setText(f'Turn #{b.turn}')

    def on_point_update(self, b: Board):
        """This function sets correct text for the labels"""
        self.player1_points_label.setText(f'Your points: {b.player1_points}')
        self.player2_points_label.setText(f'{self.opponent}s\' points: {b.player2_points}')

    def update(self, pos: tuple):
        self.board.push(pos)

