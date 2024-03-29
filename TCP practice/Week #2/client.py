import socket
import errno
import sys
import threading
import pickle

HEADER_LENGTH = 15
IP = "127.0.0.1"
SERVER_PORT = 2345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, SERVER_PORT))
client_socket.setblocking(False)

print(f"My address: {client_socket.getsockname()}\n")

my_username = input("Username: ")
target_IP =  IP#input("Target IP: ")
target_Port = int(input("Target Port: "))
target_Address = (target_IP, target_Port)

username = pickle.dumps({
            "target_address": target_Address,
            "data": my_username
        })

username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

def recieve():
    while True:
        try:
            while True:
                #receive username + message
                message_header = client_socket.recv(HEADER_LENGTH)
                
                if not len(message_header):
                    print("connection closed by the server")
                    sys.exit()
                
                message_length = int(message_header.decode("utf-8").strip())
                recieve_message = pickle.loads(client_socket.recv(message_length))
                from_username = recieve_message["username"]
                from_address = recieve_message["from_address"]
                main_message = recieve_message["data"]
                
                print(f"\n{from_username}{from_address} > {main_message}")


        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
            continue

        except Exception as e:
            print("General error", str(e))
            pass

threading.Thread(target=(recieve)).start()

while True:
    data = input(f"{my_username} > ") 

    if data:
        message = {
            "target_address": target_Address,
            "data": data
        }
        message = pickle.dumps(message)
        message_header  = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)







