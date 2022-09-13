# 一般浏览器、邮件等应用程序收发数据是用TCP；DNS查询等收发较短的控制数据是用UDP
import socket

HOST = '127.0.0.1'
PORT = 9997

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'AAABBBCCC', (HOST, PORT))

data, address = client.recvfrom(4096)
print(data.decode('utf-8'))
print(address.decode('utf-8'))

client.close()