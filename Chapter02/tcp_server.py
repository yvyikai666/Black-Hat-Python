"""可以做一个远程代码执行工具或者代理工具"""
import socket
import threading

IP = '0.0.0.0'
PORT = 9998


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))  # 指定要接听的ip和接口
    server.listen(5)  # 开始监听，最大接口数为5
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        client, address = server.accept() # 接收客户端套接字对象和远程连接的详细信息
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        # 创建并启动一个新的线程
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACKKK')


if __name__ == '__main__':
    main()
