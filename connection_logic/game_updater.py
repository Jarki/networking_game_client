import threading
import logging
import re

from connection_logic.server_communicator import ServerCommunicator
from forms.game import Game


class GameUpdater:
    def __init__(self):
        self.game = None
        self.server_comm = ServerCommunicator()

    def set_game_form(self, game_form: Game):
        self.game = game_form
        self.game.set_event_handler('update', self.send_update)

    def set_server_communicator(self, server_comm: ServerCommunicator):
        self.server_comm = server_comm

    def start_game(self, name, server_addr: tuple = ('127.0.0.1', 65432)):
        logging.debug("Trying to start the game")
        opponent, has_first_turn = self.server_comm.connect_to_game(name, server_addr)

        logging.debug(f'Opponent is {opponent}')
        self.game.set_opponent(opponent)
        logging.debug(f'Has first turn: {has_first_turn}')
        self.game.setup_board(bool(has_first_turn))

        threading.Thread(target=self.server_comm.listen_to_updates, args=[self.update_game]).start()

    def update_ping(self):
        pass

    def update_game(self, data):
        data = data.decode('utf-8')

        pattern = re.compile('push\\([0-9]+, ?[0-9]+\\)')
        if pattern.match(data) is not None:
            # message looks like push(0,0)
            data.replace('push', '')  # remove the word
            data = data[1:-1].split(',')  # remove round brackets and split
            data = map(lambda x: int(x), data)  # convert everything to int

            self.game.update(tuple(data))  # make a tuple and update
            return  # don't need the function to continue

    def send_update(self, _input):
        self.server_comm.send_message(self.game.get_text())
