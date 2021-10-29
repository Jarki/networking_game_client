import socket
import time
import threading

from connection_logic.game_updater import GameUpdater


class ServerCommunicator:
    def __init__(self):
        self.sock = None
        self.updater = GameUpdater()

    def connect_to_game(self, serv_addr: tuple, player_info):
        """server addr is a tuple (HOST, PORT)"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(serv_addr)

        self.sock.sendall(str.encode(player_info.to_string()))

    def listen_to_updates(self):
        while True:
            data = self.sock.recv(1024)
            self.updater.update_log(data)

    def send_message(self, message):
        self.sock.sendall(message)
