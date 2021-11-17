import logging
import socket
import time


class ServerCommunicator:
    def __init__(self):
        self.sock = None

    def connect_to_game(self, player_info, serv_addr: tuple):
        """server addr is a tuple (HOST, PORT)"""
        logging.debug(f'Connecting to the game')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(serv_addr)

        self.sock.sendall(b'want connect')

        if not self.sock.recv(1024) == b'connected':
            return

        self.sock.sendall(str.encode(player_info))
        logging.debug(f'Successfully connected')

    def listen_to_updates(self, callback):
        logging.debug(f'Listening to server')
        while True:
            data = self.sock.recv(1024)
            logging.debug(f'Received a message: {data}')

            callback(data)

    def send_message(self, message):
        self.sock.sendall(str.encode(message))
