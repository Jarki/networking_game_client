# #!/usr/bin/env python3
#
# import socket
# import time
# import threading
# import logging
# import os
#
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QListWidget, QMainWindow
# from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
# from PyQt5 import QtCore
# os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "platforms/"  # need to set this env var for qt to work
# #
# # logger = logging.getLogger()
# # logger.setLevel(logging.DEBUG)
# #
# # HOST = '127.0.0.1'  # The server's hostname or IP address
# # PORT = 65432  # The port used by the server
# #
# #
# # def get_data():
# #     while True:
# #         data = s.recv(1024)
# #         print(f"received: {data}")
# #
# #
# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #     s.connect((HOST, PORT))
# #     s.sendall(b'1')
# #
# #     threading.Thread(target=get_data).start()
# #
# #     for i in range(0, 35):
# #         a = input()
# #         if a != "close":
# #             start = time.perf_counter()  # start timer before sending
# #             end = time.perf_counter()  # end timer after receiving
# #
# #             print(f"elapsed: {round(end - start, 4)}s")  # ping
# #
# #             s.sendall(str.encode(a))
# #         else:
# #             break

# game_info_container = QHBoxLayout()
# main_container.addLayout(game_info_container)
#
# player_info_container = QVBoxLayout()
# game_info_container.addLayout(player_info_container)
#
# ping_label = QLabel(text='ping')
# server_address_label = QLabel('server-addr')
# opponent_info_label = QLabel('opponent')
# game_log = QListWidget()
# game_log.setGeometry(0, 0, 100, 100)
# game_log.addItem('asas')
# game_log.setMaximumWidth(int(window_size['w']/2))
# game_log.setMaximumHeight(int(window_size['h']/2))
#
# player_info_container.addWidget(ping_label)
# player_info_container.addWidget(server_address_label)
# game_info_container.addWidget(game_log)
#
# game_action_container = QVBoxLayout()
# game_action_container.setAlignment(QtCore.Qt.AlignCenter)
#
# message_input = QLineEdit()
# message_input.setMaximumWidth(256)
# message_button = QPushButton('Send message')
#
# game_action_container.addWidget(message_input)
# game_action_container.addWidget(message_button)
# main_container.addLayout(game_action_container)

import app

a = app.App()
a.run()
