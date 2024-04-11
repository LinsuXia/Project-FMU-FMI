import socket
import pickle
import json
import threading



# ----------------------------------------------------------
class Node:
    def __init__(self,node_name:str,input:list,output:list,_socket:socket = None,step_size:str = "0.01",start_time:str = "0"):
        self.node_name = node_name
        self.input = input
        self.output = output

        self.socket = _socket

        self.step_size = step_size
        self.curr_time = start_time

        #send_data to this Node
        self.input_data = []
        #recv_data from this Node
        self.output_data = []

    def load_socket(self,_socket:socket):
        if self.socket is None:
            self.socket = _socket
        else:
            print("{} has loaded a socket, you are trying modifying it")
            self.socket.close()
            self.socket = _socket

    #need a lock ? continue to update
    #refresh output_data and curr_time after recv data
    #the data format must be a string
    #output_data1,output_data2,....,time
    def refresh_ouput_data(self,recv_data:str):
        if recv_data is None:
            return
        recv_data = recv_data.split(',')
        if len(recv_data) is not len(self.input) + 1:
            raise Exception("{} recv wrong data".format(self.node_name))
        else:
            self.output_data.clear()
            self.output_data = recv_data[:-1]

        if recv_data[-1]<self.curr_time:
            raise Exception("{} recv wrong data".format(self.node_name))
        else:
            self.curr_time = recv_data[-1]

    #you are supposed to get curr_time with this func
    def get_curr_time(self):
        return self.curr_time

    #you are supposed to get input_data(send_data) with this func
    #the send_data must be a string
    #input_data1,input_data2,....
    def get_input_data(self)->str:
        send_data = ""
        if len(self.input_data) != len(input):
            raise Exception("{} sends wrong data".format(self.node_name))
            
        for _input_data in self.input_data:
            send_data += _input_data +","

        return send_data[:-1]

    #if socket is loaded return true
    def is_Node_available(self)->bool:
        if self.socket is not None: 
            return True
        else:
           return False


# ----------------------------------------------------------
class Link:
    def __init__(self,name:str,begin_node:Node,end_node:Node,begin_port:str,end_port:str):
        self.link_name = name
        self.begin_node = begin_node
        self.end_node = end_node
        self.begin_port = begin_port
        self.end_port = end_port

        self.begin_port_index = "-1"
        self.end_port_index = "-1"

    def get_begin_node(self):
        return self.begin_node

    def get_end_node(self):
        return self.end_node

    def get_begin_port_index(self):
        if self.begin_port_index == "-1":
            index = self.begin_port.strip("{}O".format(self.begin_node.node_name))

            if(index.isdigit()):
                self.begin_port_index = index
                return index
            else:
                raise Exception("{}'s begin_port is wrong".format(self.link_name))
        else:
           return self.begin_port_index

    def get_end_port_index(self):
        if self.end_port_index == "-1":
            index = self.end_port.strip("{}I".format(self.end_node.node_name))

            if(index.isdigit()):
                self.end_port_index = index
                return index
            else:
                raise Exception("{}'s end_port is wrong".format(self.link_name))
        else:
            return self.end_port_index
           


nodes = {}
# ----------------------------------------------------------
# recv message should be a string
#接受的信息格式为data1,data2.....,time
#这个位置我们接受2进制信息的时候长度应该是固定的
#这个位置还需要后续更新
def recieve_message(client_socket:socket,standard_length:int = 1024)->str:
    try:
        message = client_socket.recv(standard_length).decode('utf-8')
        message = pickle.loads(message)
        return message
        
    except:
        return ""

# ---------------------------------------------------------------------------------
#linking function, target of main thread
#这个位置我没动
#所以这个函数暂时跑不通，需要你们根据我其他的修改来重写
#目前我的想法是做2个函数
#第一个函数是在初始化完link_dict之后，我们直接开启link_num个线程，用于更新beginport->endport的信息传输
#在这个函数while条件里写上，当且仅当beginNode.scoket is not None and endNode.socket is not None 才开始起作用
#第二个函数是在收到一个accept一个node之后，开启一个线程用来接收这个node从client传入的信息
def linking(beginNode_socket, endPort_socket):
    global nodes
    while True:
        #recieve
        message = recieve_message(beginNode_socket)
        if message is False:
            print(f"Closed connction from {nodes[beginNode_socket]}")
        nodeName = nodes[beginNode_socket]
        for check_socket in nodes:
            if (check_socket.getpeername()[0] == endPort_socket.getpeername()[0]) and (check_socket.getpeername()[1] == endPort_socket.getpeername()[1]):
                #add info and send
                message["beginNode"] = nodeName
                send_message = pickle.dumps(message)
                print(f"Sending message from {nodeName} {beginNode_socket.getpeername()} to {nodes[check_socket]} {check_socket.getpeername()}")
                check_socket.send(f"{len(send_message):<{HEADER_LENGTH}}".encode("utf-8") + send_message)

# --------------------------------------------------------------------------------------

#
def json_data_preprocess(settings):
    #serverIP这个在配置文件里也是有的，需要去获取，如果你们要用127.0.0.1测试的话需要修改一下文件
    ip = settings["severIP"]
    port = 2345

    link_lists = settings["linkLists"]
    link_num = settings["linkNum"]

    node_lists = settings["nodeLists"]
    node_num = settings["nodeNum"]

    node_dict = {}
    link_dict = {}

    for i in range(int(node_num)):
        node_dict[node_lists[i]["nodeName"]] = Node(node_lists[i]["nodeName"],node_lists[i]["input"],node_lists[i]["output"])

    for i in range(int(link_num)):
        begin_node = node_dict.get(port2node(link_lists[i]["beginPort"],True))
        end_node = node_dict.get(port2node(link_lists[i]["endPort"]))
        if begin_node is not None and end_node is not None:
            link_dict[link_lists[i]["Name"]] = Link(link_lists[i]["Name"],begin_node,end_node,link_lists[i]["beginPort"],link_lists[i]["endPort"])

    return ip,port,node_dict,link_dict

def port2node(port:str,is_begin_port:bool = False)->str:
    if is_begin_port:
        cnt:int = 0
        for i in range(len(port)-1, -1, -1):
            cnt += 1
            if port[i] == 'O':
                break   
        return "node"+port[:-cnt]
    else:
        cnt:int = 0
        for i in range(len(port)-1, -1, -1):
            cnt += 1
            if port[i] == 'I':
                break   
        return "node"+port[:-cnt]

# --------------------------------------------------------------------------------------
#accept new node
def main(settings_file_path:str = "settings.json"):
    #json file load
    with open(settings_file_path, 'r') as file:
        settings = json.load(file)
    
    #data preprocess
    ip,port,node_dict,link_dict = json_data_preprocess(settings)
    #server socket init and wait for client
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(0)
    print("Service started, waiting for client")

    while True:
        node_socket, node_address = server_socket.accept()
        #收到的第一条信息为这个节点的名字
        #这里的"\x00"是填充信息，因为.cpp,.c的send的长度是一个定长，需要用\x00填充到固定长度，可以先不用管这一行
        node_name = node_socket.recv(1024).decode('utf-8').split("\x00")[0]
        print("{} connected".format(node_name))
        
        if(node_name in node_dict.keys()):
            node_dict[node_name].load_socket(node_socket)
        else:
            node_socket.close()
            print("Unknown client rejected!")

    #    #下面这个部分的linking函数需要再考虑一下
    #    print(f"Accepted new connection from {node_address[0]}:{node_address[1]} nodename:{node_name}")
    #    threading.Thread(target=(linking), args=(node_socket, endPort_socket)).start()

# ----------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    main("sample1.json")