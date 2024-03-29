import socket
import select
import pickle

HEADER_LENGTH = 15
IP = "127.0.0.1"
PORT = 2345

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #使得客户端可以重连（？）

server_socket.bind((IP, PORT))
server_socket.listen(5)
print("Service started, waiting for client")

socket_list = [server_socket]

clients = {}
# ----------------------------------------------------------
def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        message = client_socket.recv(message_length)
        message = pickle.loads(message)
        return message
            
    except:
        return False
# ---------------------------------------------------------------------------------


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list) #select.select()函数会监视套接字列表，三个返回值分别是可读套接字列表、可写套接字列表、出错套接字 列表（这里用_表示忽略）

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            
            if recieve_message(client_socket) is False:
                continue

            username = recieve_message(client_socket)["data"]
            
            socket_list.append(client_socket)
            clients[client_socket] = username
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{username}")



        else:
            message = recieve_message(notified_socket)
            if message is False:
                print(f"Closed connction from {clients[notified_socket]}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            username = clients[notified_socket]
            target_address = message["target_address"]
            
            for send_socket in clients:
                if (send_socket.getpeername()[0] == target_address[0]) and (send_socket.getpeername()[1] == target_address[1]):
                    message["username"] = username
                    message["from_address"] = notified_socket.getpeername()
                    send_message = pickle.dumps(message)
                    print(f"Sending message from {username} {notified_socket.getpeername()} to {clients[send_socket]} {send_socket.getpeername()}")
                    send_socket.send(f"{len(send_message):<{HEADER_LENGTH}}".encode("utf-8") + send_message)
    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
