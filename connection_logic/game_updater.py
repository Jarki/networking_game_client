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
        self.game.set_event_handler('message', self.send_message)

    def set_server_communicator(self, server_comm: ServerCommunicator):
        self.server_comm = server_comm

    def start_game(self, name, server_addr: tuple = ('127.0.0.1', 65432)):
        logging.debug("Starting the game")

        self.server_comm.connect_to_game(name, server_addr)
        self.game.set_player(name)
        self.game.setup_board()

        threading.Thread(target=self.server_comm.listen_to_updates, args=[self.update_game]).start()

    def update_ping(self):
        pass

    def update_game(self, data):
        data = data.decode('utf-8')

        if data == '':
            return

        for entry in data.split('/%%'):
            logging.debug(entry)

            pattern = re.compile('push\\([0-9]+, ?[0-9]+\\)')
            if pattern.match(entry) is not None:
                # message looks like push(0,0)
                entry = entry.replace('push', '')  # remove the word push
                entry = entry[1:-1].split(',')  # remove round brackets and split
                entry = map(lambda x: int(x), entry)  # convert everything to int

                logging.debug("Push")
                self.game.update(tuple(entry))  # make a tuple and update
                return  # don't need the function to continue

            if entry == 'wait':
                self.game.update_chat('Waiting for second player...')

            pattern = re.compile('msg:[a-zA-Z1-9]+:.+')
            if pattern.match(entry) is not None:
                # message looks like msg:player1:hello
                msg = entry.replace('msg:', '')  # remove the word msg
                logging.debug(f'Message: {msg}')
                self.game.update_chat(msg)  # display message in chat
                return  # don't need the function to continue

            pattern = re.compile('opponent:[a-zA-Z1-9]+')
            if pattern.match(entry) is not None:
                # message looks like Opponent:player1
                opponent = entry.replace('opponent:', '')  # remove the word Opponent
                logging.debug(f'Opponent is {opponent}')
                self.game.set_opponent(opponent)  # set opponent
                self.game.update_chat(f'Opponent is {opponent}')
                return  # don't need the function to continue

            pattern = re.compile('start:[a-zA-Z1-9]+')
            if pattern.match(entry):
                # message looks like Opponent:player1
                starts = entry.replace('start:', '')  # remove the word start to know who has first turn
                if starts != self.game.opponent:
                    self.game.board.toggle_active_player()

    def send_update(self, _input):
        update = f'push({_input[0]},{_input[1]})'

        self.server_comm.send_message(update)

    def send_message(self, message):
        self.server_comm.send_message(f'msg:{self.game.player}:{message}')
