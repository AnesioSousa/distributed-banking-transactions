import socket

DEBUG = False
PORT = 65136
PROCESSES_QUANTITY = 3
ENV_HOST = f"http://{socket.gethostbyname(socket.gethostname())}"
