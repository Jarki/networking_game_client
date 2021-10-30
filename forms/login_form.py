from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QListWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt


class LoginForm():
    def __init__(self, container_widget):
        self.container = container_widget
        self.container.window().setWindowTitle('Login')
        width = 450
        height = 270
        self.container.window().setGeometry(200, 200, width, height)

        # wrapper for all widgets in the form
        self.wrapper = QVBoxLayout()
        self.wrapper.setAlignment(Qt.AlignCenter)
        self.container.setLayout(self.wrapper)

        # labels
        self.name_label = QLabel(text='Your name:')
        self.server_address_label = QLabel('Server address:')

        # line edits

        self.name_input = QLineEdit()
        self.name_input.setMaximumWidth(256)
        self.server_address_input = QLineEdit()
        self.server_address_input.setMaximumWidth(256)

        # button
        self.join_button = QPushButton('Join game')

        # place everything
        self.wrapper.addWidget(self.name_label)
        self.wrapper.addWidget(self.name_input)
        self.wrapper.addWidget(self.server_address_label)
        self.wrapper.addWidget(self.server_address_input)
        self.wrapper.addWidget(self.join_button)

    def get_name_input(self):
        return self.name_input.text()

    def get_server_addr_input(self):
        return self.server_address_input.text()

    def add_join_button_handler(self, func):
        self.join_button.clicked.connect(func)
