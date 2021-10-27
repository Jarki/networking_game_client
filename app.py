from main_window import MainWindow
from forms.game_form import GameForm

import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


class App:
    def __init__(self):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "platforms/"

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
        GameForm(self.central_widget)

    def run(self):
        self.window.show()
        self.app.exec()
