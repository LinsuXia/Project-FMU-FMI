from socket import *

# todo 1、客户端、创建client-socket    TCP协议
client_socket = socket(AF_INET, SOCK_STREAM)

# todo  2、客户端发送连接的请求（不是传输数据的请求，是创建连接的请求）

# todo  目标服务器的ip和端口号
server_ip_port = ('172.20.10.2', 8888)

# todo 发送连接请求，此时服务端产生了新的new_socket
client_socket.connect(server_ip_port)

#client_socket.close()

# todo 客户端发送请求,用send不用sendto，客户端知道服务器的ip和端口，服务器也知道客户端的端口和ip，因为是面向连接的
send_data = input('请输入：')
client_socket.send(send_data.encode('utf-8'))

# todo  接收服务器返回的数据
recv_data = client_socket.recv(1024)

print('客户端接收到的服务器的数据为：', recv_data.decode(encoding='utf-8'))

# todo 关闭socket
client_socket.close()