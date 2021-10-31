from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QListWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

from forms.basic_form import BasicForm


class GameForm(BasicForm):
    def __init__(self, container_layout, container_widget):
        super().__init__()
        self.container = container_layout

        width = container_widget.geometry().width()
        height = container_widget.geometry().height()

        # wrapper for all widgets in the form
        self.wrapper = QVBoxLayout()
        self.container.addLayout(self.wrapper)

        # game info container
        self.game_info_container = QHBoxLayout()

        # container for all of the info about player
        self.player_info_container = QVBoxLayout()

        # labels
        self.ping_label = QLabel(text='ping')
        self.server_address_label = QLabel('server-addr')
        self.opponent_info_label = QLabel('opponent')

        self.player_info_container.addWidget(self.ping_label)
        self.player_info_container.addWidget(self.server_address_label)
        self.player_info_container.addWidget(self.opponent_info_label)

        # list widget to keep track of player actions
        self.game_log = QListWidget()
        self.game_log.setMaximumWidth(int(width / 2))
        self.game_log.setMaximumHeight(int(height / 2))

        # place everything
        self.game_info_container.addLayout(self.player_info_container)
        self.game_info_container.addWidget(self.game_log)
        self.wrapper.addLayout(self.game_info_container)

        # create a container for inputs
        self.game_action_container = QVBoxLayout()
        self.game_action_container.setAlignment(Qt.AlignCenter)

        # create inputs
        self.message_input = QLineEdit()
        self.message_input.setMaximumWidth(256)
        self.message_button = QPushButton('Send message')

        self.game_action_container.addWidget(self.message_input)
        self.game_action_container.addWidget(self.message_button)

        self.wrapper.addLayout(self.game_action_container)

    def update_ping(self, number):
        self.ping_label.setText(f'Ping: {number} ms')

    def update_opponents_name(self, name):
        self.opponent_info_label.setText(f'Opponent: {name}')

    def update_server_address(self, address):
        self.server_address_label.setText(f'Server address: {address}')

    def update_log(self, msg):
        self.game_log.addItem(msg)

    def set_button_handler(self, func):
        self.message_button.clicked.connect(func)

    def get_text(self):
        return self.message_input.text()
