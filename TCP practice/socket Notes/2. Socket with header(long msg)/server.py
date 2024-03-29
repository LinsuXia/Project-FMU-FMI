import socket
import time 
import datetime

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection  fromn {address} has been established")

    msg = "Welcome to the server!"
    msg = f"{len(msg):<{HEADERSIZE}}" + msg

    clientsocket.send(bytes(msg, "utf-8"))
    while True:
        time.sleep(3)
        msg = f"The time is: {datetime.datetime.now()}"
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        clientsocket.send(bytes(msg, "utf-8"))
