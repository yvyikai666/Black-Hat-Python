"""用来测试服务,发送垃圾数据,进行fuzz"""
# 套接字（socket）原意是插座插口的意思，是对网络中不同主机上的应用进程双向通信的端口的抽象，也就是管道两端的数据出入口。
import socket

# IP地址和端口号是客户端和服务端之间用来识别对方套接字的机制
HOST = "www.baidu.com"
PORT = 80  # web服务器的端口号都是80

# creat a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET表示使用标准的ipv4,sock_stream表示是一个TCP客户端

# connect the client
client.connect((HOST, PORT))

# send some data
client.send(b'GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n')

# receive some data
response = client.recv(4096)

print(response.decode('utf-8'))
client.close()

"""
一般来说收发数据的操作分为4个阶段：
  1. 创建套接字
  2. 将管道连接到服务器端的套接字上
  3. 收发数据
  4. 断开管道，并删除套接字
"""
