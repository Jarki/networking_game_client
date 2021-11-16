from main_window import MainWindow
from forms.game_form import GameForm
from forms.login_form import LoginForm
from forms.game import Game
import connection_logic as cl
from player import Player
from game.board import Board

import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QHBoxLayout


class App:
    def __init__(self):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "platforms/"

        self.app = QApplication([])

        self.__create_window()

        # self.login_form = LoginForm(self.main_container, self.central_widget)
        # self.login_form.add_join_button_handler(self.__get_login_form_inputs)

        self.__initialize_game_form()

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

    def __initialize_game_form(self):
        self.gf = Game(self.main_container, self.central_widget)

        self.gu = cl.GameUpdater()
        self.gu.set_game_form(self.gf)

        self.gu.start_game('Josh')

    def __get_login_form_inputs(self):
        self.player = Player(self.login_form.get_name_input())
        self.server_addr = self.login_form.get_server_addr_input().split(':')
        #self.server_addr[1] = int(self.server_addr[1])
        #self.server_addr = tuple(self.server_addr)

        self.login_form.clear()
        self.__initialize_game_form()

    def run(self):
        self.window.show()
        self.app.exec()
