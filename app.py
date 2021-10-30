from main_window import MainWindow
from forms.game_form import GameForm
from forms.login_form import LoginForm
import connection_logic as cl
from player import Player

import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


class App:
    def __init__(self):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "platforms/"

        # self.__initialize_game_form()

        self.app = QApplication([])
        self.window = MainWindow()

        self.window_size = {
            'w': 1080,
            'h': 500
        }

        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)

        self.window.setWindowTitle('Game')
        self.window.setGeometry(300, 300, self.window_size['w'], self.window_size['h'])
        self.central_widget.setGeometry(0, 0, self.window_size['w'], self.window_size['h'])

        self.login_form = LoginForm(self.central_widget)
        self.login_form.add_join_button_handler(self.__get_login_form_inputs)

    def __initialize_game_form(self):
        self.__clear_window()

        self.gf = GameForm(self.central_widget)
        self.sc = cl.ServerCommunicator()
        self.sc.connect_to_game(('127.0.0.1', 65432), "bob")

        self.gu = cl.GameUpdater()
        self.gu.set_game_form(self.gf)
        self.gu.set_server_communicator(self.sc)

    def __get_login_form_inputs(self):
        self.player = Player(self.login_form.get_name_input())
        self.server_addr = self.login_form.get_server_addr_input()

        self.__initialize_game_form()

    def __clear_window(self):
        pass

    def run(self):
        self.window.show()
        self.app.exec()
