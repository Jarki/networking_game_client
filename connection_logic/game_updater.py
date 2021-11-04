import threading
import logging

from connection_logic.server_communicator import ServerCommunicator
from forms.game_form import GameForm


class GameUpdater:
    def __init__(self):
        self.game_form = None
        self.server_comm = None

    def set_game_form(self, game_form: GameForm):
        self.game_form = game_form
        self.game_form.set_button_handler(self.get_input)

    def set_server_communicator(self, server_comm: ServerCommunicator):
        self.server_comm = server_comm
        threading.Thread(target=self.server_comm.listen_to_updates, args=[self.update_log]).start()

    def update_ping(self):
        pass

    def update_log(self, data):
        self.game_form.update_log(data.decode('utf-8'))

    def get_input(self, _input):
        self.server_comm.send_message(self.game_form.get_text())
