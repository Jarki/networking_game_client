from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

import threading
import logging
import re
import time

from connection_logic.server_communicator import ServerCommunicator
from forms.game import Game
from forms.size_chooser_form import SizeChooserForm
from forms.waiting_form import WaitingForm


class GameUpdater:
    def __init__(self):
        self.game = None
        self.server_comm = ServerCommunicator()
        self.game_container = None
        self.size_form = None
        self.waiting_form = None

        self.show_size_form = False
        self.show_game_form = False

    def create_game_in(self, container_widget):
        self.game_container = container_widget
        self.game = Game(container_widget)

        self.game.set_event_handler('update', self.send_update)
        self.game.set_event_handler('message', self.send_message)
        self.game.set_event_handler('end_game', self.vote_end_game)

    def start_game(self, name, server_addr: tuple = ('127.0.0.1', 65432), board_size=10):
        logging.debug("Starting the game")

        self.server_comm.connect_to_game(name, server_addr)
        self.game.set_player(name)

        threading.Thread(target=self.listen_to_updates).start()
        self.waiting_form = WaitingForm(self.game_container)

        self.wait_for_response()

    def wait_for_response(self):
        while True:
            QtCore.QCoreApplication.processEvents()

            if self.show_size_form:
                if self.waiting_form is not None:
                    self.waiting_form.clear()

                self.size_form = SizeChooserForm(self.game_container)
                self.size_form.set_button_handler(self.__get_radius)
                return

            if self.show_game_form:
                if self.waiting_form is not None:
                    self.waiting_form.clear()
                if self.size_form is not None:
                    self.size_form.clear()

                self.game.show()
                self.game.draw_board()

                return

    def __get_radius(self):
        radius = 0

        try:
            radius = int(self.size_form.get_radius())
        except ValueError:
            msg = QMessageBox()
            msg.setText('Радіус повинен бути числом')
            msg.exec()
            return

        if radius < 1 or radius > 10:
            msg = QMessageBox()
            msg.setText('Радіус повинен знаходитись в радіусі(1, 10)')
            msg.exec()
            return

        self.server_comm.send_message(f'size:{radius}')

        self.show_size_form = False

        self.size_form.clear()
        self.waiting_form = WaitingForm(self.game_container)

        self.wait_for_response()

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
            if entry == '':
                continue

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

            if entry == 'choose':
                self.show_size_form = True

            if entry == "size":
                pass

            if entry.startswith('stats:'):
                entry = entry.split(':')

                wins = entry[1]
                losses = entry[2]
                draws = entry[3]

                self.game.set_stats(tuple([wins, losses, draws]))
                continue

            if entry.startswith('size:'):
                size = entry.replace('size:', '')
                size = int(size)
                self.game.setup_board(size * 2)

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

                self.game.set_opponent(opponent)  # set opponent
                self.game.update_chat(f'Opponent is {opponent}')
                continue  # don't need the function to continue

            pattern = re.compile('start:[a-zA-Z1-9]+')
            if pattern.match(entry):
                # message looks like start:player1
                starts = entry.replace('start:', '')  # remove the word start to know who has first turn
                self.show_game_form = True

                time.sleep(0.2)

                print(f'starting the game is {starts}')
                print(f'opponent is {self.game.opponent}')
                if starts != self.game.opponent:
                    self.game.board.active_player = True

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
