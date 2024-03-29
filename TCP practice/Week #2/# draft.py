import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 1234))

print(s)
print(s.getsockname())
print(s.getsockname()[0])
print(s.getsockname()[1])