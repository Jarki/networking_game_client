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
        self.game.set_event_handler('end_game', self.vote_end_game)

    def start_game(self, name, server_addr: tuple = ('127.0.0.1', 65432)):
        logging.debug("Starting the game")

        self.server_comm.connect_to_game(name, server_addr)
        self.game.set_player(name)
        self.game.setup_board()

        threading.Thread(target=self.listen_to_updates).start()

    def vote_end_game(self, msg):
        self.server_comm.send_message(msg)

    def listen_to_updates(self):
        logging.debug(f'Listening to server')
        while True:
            try:
                self.server_comm.listen_to_updates(self.update_game)
            except ServerCommunicator.ZeroBytesReceivedError as e:
                print(str(e))
                break
            except ConnectionResetError:
                print('Server connection closed')
                break

    def update_ping(self):
        pass

    def update_game(self, data):
        data = data.decode('utf-8')

        if data == '':
            return

        for entry in data.split('/%%'):
            pattern = re.compile('push\\([0-9]+, ?[0-9]+\\)')
            if pattern.match(entry) is not None:
                # message looks like push(0,0)
                logging.debug(entry)
                entry = entry.replace('push', '')  # remove the word push
                entry = entry[1:-1].split(',')  # remove round brackets and split
                entry = map(lambda x: int(x), entry)  # convert everything to int

                self.game.update(tuple(entry))  # make a tuple and update
                continue  # don't need the function to continue

            if entry == 'wait':
                self.game.update_chat('Waiting for second player...')
                continue

            if entry.startswith('stats:'):
                entry = entry.split(':')

                wins = entry[1]
                losses = entry[2]
                draws = entry[3]

                self.game.set_stats(tuple([wins, losses, draws]))
                continue

            pattern = re.compile('msg:[a-zA-Z1-9]+:.+')
            if pattern.match(entry) is not None:
                # message looks like msg:player1:hello
                msg = entry.replace('msg:', '')  # remove the word msg
                logging.debug(f'Message: {msg}')
                self.game.update_chat(msg)  # display message in chat
                continue  # don't need the function to continue

            pattern = re.compile('opponent:[a-zA-Z1-9]+')
            if pattern.match(entry) is not None:
                # message looks like Opponent:player1
                opponent = entry.replace('opponent:', '')  # remove the word Opponent
                logging.debug(f'Opponent is {opponent}')
                self.game.set_opponent(opponent)  # set opponent
                self.game.update_chat(f'Opponent is {opponent}')
                continue  # don't need the function to continue

            pattern = re.compile('start:[a-zA-Z1-9]+')
            if pattern.match(entry):
                # message looks like start:player1
                starts = entry.replace('start:', '')  # remove the word start to know who has first turn
                if starts != self.game.opponent:
                    self.game.board.toggle_active_player()

                continue

            pattern = re.compile('winner:.+')
            if pattern.match(entry):
                # message looks like winner:player1
                logging.debug(entry)
                winner = entry.replace('winner:', '')  # remove the word winner to know who has won
                if winner == self.game.opponent:
                    self.game.set_winner('You have lost')
                elif winner == ':draw:':
                    self.game.set_winner('Draw')
                else:
                    self.game.set_winner('You have won')
                self.game.set_game_status('Game has ended')

                continue

            if entry == 'leave' or entry == 'unleave':
                self.game.update_chat(f'{self.game.opponent} voted to {entry}')

                continue

    def send_update(self, _input):
        update = f'push({_input[0]},{_input[1]})'

        self.server_comm.send_message(update)

    def send_message(self, message):
        self.server_comm.send_message(f'msg:{self.game.player}:{message}')
