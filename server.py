import socket
import threading

lock = threading.Lock()


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 2345


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind((IP, PORT))
server_socket.listen(0)
ports = {}

def linking(begin_socket):
    global ports
    message = begin_socket.recv(1024)
    while True:
        lock.acquire()
        for port in ports:
            if ports[port] != begin_socket:
                ports[port].send(message)
        lock.release()



def main():
    client_socket, client_address = server_socket.accept()
    port_name = client_socket.recv(1024)
    ports[port_name] = client_socket
    
    threading.Thread(target=(linking), args=(client_socket,))
    return

main()