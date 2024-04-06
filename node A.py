import socket
import time

HEADER_LENGTH = 10
IP = "127.0.0.1"
SERVER_PORT = 2345
PORTNAME = "Port A"
INPUT_PORT1 = "AI1"
INPUT_PORT2 = "AI2"
OUTPUT_PORT1 = "AO1"
OUTPUT_PORT2 = "AO2"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, SERVER_PORT))


client_socket.send(PORTNAME)
current_time = 0
msgNO = 0

# main
while True:
    current_time +=0.1
    msgNO += 1
    message = f"{msgNO},{current_time}"
    client_socket.send(message)
    recieve_message = client_socket.recv(1024).split(",")
    main_message = recieve_message[0]
    another_time = recieve_message[1]

    print(f"Recieved message from Port B: {main_message} , another time: {another_time}")
    time.sleep(1)


    









