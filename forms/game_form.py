from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QListWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class GameForm:
    def __init__(self, container_widget):
        self.container = container_widget

        print(self.container.geometry())
        width = 1080
        height = 720

        self.game_info_container = QHBoxLayout()
        self.container.setLayout(self.game_info_container)

        self.player_info_container = QVBoxLayout()
        self.game_info_container.addLayout(self.player_info_container)

        self.ping_label = QLabel(text='ping')
        self.server_address_label = QLabel('server-addr')
        self.opponent_info_label = QLabel('opponent')
        self.game_log = QListWidget()
        self.game_log.setGeometry(0, 0, 100, 100)
        self.game_log.addItem('asas')
        self.game_log.setMaximumWidth(int(width / 2))
        self.game_log.setMaximumHeight(int(height / 2))

        self.player_info_container.addWidget(self.ping_label)
        self.player_info_container.addWidget(self.server_address_label)
        self.game_info_container.addWidget(self.game_log)

        self.game_action_container = QVBoxLayout()
        self.game_action_container.setAlignment(Qt.AlignCenter)

        self.message_input = QLineEdit()
        self.message_input.setMaximumWidth(256)
        self.message_button = QPushButton('Send message')

        self.game_action_container.addWidget(self.message_input)
        self.game_action_container.addWidget(self.message_button)
        self.game_info_container.addLayout(self.game_action_container)