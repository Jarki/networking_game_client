import socket
import time


class ServerCommunicator:
    def __init__(self):
        self.sock = None

    def connect_to_game(self, serv_addr: tuple, player_info):
        """server addr is a tuple (HOST, PORT)"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(serv_addr)

        self.sock.sendall(b'want connect')

        if not self.sock.recv(1024) == b'connected':
            return

        self.sock.sendall(str.encode(player_info))

    def listen_to_updates(self, callback):
        while True:
            data = self.sock.recv(1024)
            callback(data)

    def send_message(self, message):
        self.sock.sendall(str.encode(message))
