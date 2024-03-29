import socket
import errno
import sys
import pickle
import time

HEADER_LENGTH = 15
IP = "127.0.0.1"
SERVER_PORT = 2345
PACKAGE = "hello"
NODENAME = "nodeA"
INPUT_PORT1 = "AI1"
INPUT_PORT2 = "AI2"
OUTPUT_PORT1 = "AO1"
OUTPUT_PORT2 = "AO2"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, SERVER_PORT))
client_socket.setblocking(False)
nodeName = pickle.dumps({
            "data": NODENAME
        })

username_header = f"{len(nodeName):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + nodeName)
#main
while True:
    try:
        while True: 
            
            data = input("> ")
            if data:
                message = {
                    "data": data,
                    "beginPort": OUTPUT_PORT1
                }
                message = pickle.dumps(message)
                message_header  = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
                client_socket.send(message_header + message)
            message_header = client_socket.recv(HEADER_LENGTH)
            
            if not len(message_header):
                print("connection closed by the server")
                sys.exit()
            
            message_length = int(message_header.decode("utf-8").strip())
            recieve_message = pickle.loads(client_socket.recv(message_length))
            beginNode = recieve_message["beginNode"]
            beginPort = recieve_message["beginPort"]

            main_message = recieve_message["data"]

            print(f"Recieved message from node {beginNode} port{beginPort}: {main_message}")
            time.sleep(5)

    except IOError as e:
        if e.errno != errno .EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General error", str(e))
        pass


    









