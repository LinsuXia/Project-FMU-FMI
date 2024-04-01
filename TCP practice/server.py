import socket
import pickle
import json
import threading

HEADER_LENGTH = 15
IP = "127.0.0.1"
PORT = 2345

with open("settings.json", 'r') as file:
    SETTINGS = json.load(file)
print("file loaded")
linkLists = SETTINGS["linkLists"]
linkNum = SETTINGS["linkNum"]
nodeLists = SETTINGS["nodeLists"]

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind((IP, PORT))
server_socket.listen(5)
print("Service started, waiting for client")

nodes = {}
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
    
def linking(beginNode_socket,):
    global nodes
    global nodeLists
    global linkLists

    while True:
        #recieve
        message = recieve_message(beginNode_socket)
        if message is False:
            print(f"Closed connction from {nodes[beginNode_socket]}")
            for node in nodeLists:
                if node["socket"] == beginNode_socket:
                    del node["socket"]
            del nodes[beginNode_socket]
            continue

        nodeName = nodes[beginNode_socket]
        beginPort = message["beginPort"]
        
        #search and send
        indic = 0
        endPort_socket = False

        for link in linkLists:
            if link["beginPort"] == beginPort:
                indic = 1
                endPort = link["endPort"]
                for node in nodeLists:
                    for input_port in node["input"]:
                        if input_port == endPort:
                            try:
                                endPort_socket = node["socket"]
                            except:
                                endPort_socket = False
                            break
                    if endPort_socket:
                        break
        
        if indic == 0:
            beginNode_socket.send(f'{len("Invalid Port"):<{HEADER_LENGTH}}'.encode('utf-8') + 'Invalid Port'.encode('utf-8'))
            continue
        
        if endPort_socket == False:
            beginNode_socket.send(f'{len("Target node not connected"):<{HEADER_LENGTH}}'.encode('utf-8') + 'Target node not connected'.encode('utf-8'))
            continue

        

        for check_socket in nodes:
            if (check_socket.getpeername()[0] == endPort_socket.getpeername()[0]) and (check_socket.getpeername()[1] == endPort_socket.getpeername()[1]):
                #add info and send
                message["beginNode"] = nodeName
                send_message = pickle.dumps(message)
                print(f"Sending message from {nodeName} {beginNode_socket.getpeername()} to {nodes[check_socket]} {check_socket.getpeername()}")
                check_socket.send(f"{len(send_message):<{HEADER_LENGTH}}".encode("utf-8") + send_message)

# --------------------------------------------------------------------------------------
#accept new node
while True:
    node_socket, node_address = server_socket.accept()
    print("new client noticed")
    first_message = recieve_message(node_socket)
    if first_message is False:
        continue
    else:
        nodeName = first_message["data"]

        
        indic = 0
        for node in nodeLists:
            if node["nodeName"] == nodeName:
                node["socket"] = node_socket
                indic = 1
        if indic == 0:
            node_socket.close()
            print("Unknown client rejected!")
        nodes[node_socket] = nodeName

        print(f"Accepted new connection from {node_address[0]}:{node_address[1]} nodename:{nodeName}")
        threading.Thread(target=(linking), args=(node_socket,)).start()

# ----------------------------------------------------------------------------------------------------