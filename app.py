from main_window import MainWindow
from forms.login_form import LoginForm
from forms.game import Game
import connection_logic as cl
from player import Player

import os
import socket

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox


class App:
    def __init__(self):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "platforms/"

        self.app = QApplication([])

        self.__create_window()

        self.login_form = LoginForm(self.main_container, self.central_widget)
        self.login_form.add_join_button_handler(self.__get_login_form_inputs)

        self.server_addr: tuple[str, int] = ("127.0.0.1", 65432)

    def __create_window(self):
        self.window = MainWindow()

        self.window_size = {
            'w': 1080,
            'h': 500
        }

        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)

        self.window.setGeometry(300, 300, self.window_size['w'], self.window_size['h'])
        self.central_widget.setGeometry(0, 0, self.window_size['w'], self.window_size['h'])

        self.main_container = QHBoxLayout()
        self.central_widget.setLayout(self.main_container)

    def __get_login_form_inputs(self):
        self.player = Player(self.login_form.get_name_input())

        if self.login_form.get_server_addr_input() != "":
            try:
                server_addr = self.login_form.get_server_addr_input().split(':')
                server_addr[1] = int(server_addr[1])
                server_addr = tuple(server_addr)
                self.server_addr = server_addr
                print(self.server_addr)
            except IndexError:
                msg = QMessageBox()
                msg.setText("Wrong address.")
                msg.addButton(QMessageBox.Ok)
                msg.exec()
                return

        self.__start_game()

    def __start_game(self):
        self.gu = cl.GameUpdater()

        self.gf = Game(self.main_container, self.central_widget)

        self.gu.set_game_form(self.gf)
        try:
            self.gu.start_game(self.player.name, self.server_addr)
        except socket.gaierror:
            msg = QMessageBox()
            msg.setText("Could not connect to the server")
            msg.addButton(QMessageBox.Ok)
            msg.exec()
            return

        self.login_form.clear()
        self.gf.build(self.main_container, self.central_widget)

    def run(self):
        self.window.show()
        self.app.exec()
