# #!/usr/bin/env python3
#
# import socket
# import os
# #
# # HOST = '127.0.0.1'  # The server's hostname or IP address
# # PORT = 65432  # The port used by the server

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
