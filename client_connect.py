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

import app

a = app.App()
a.run()
