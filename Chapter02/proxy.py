"""一个TCP代理：用它在主机之间转发流量，或检测一些网络软件；分析未知协议，篡改应用的网络流量，或为fuzzer创建测试用例"""
import sys
import socket
import threading

# 这个是个布尔短路，类似于三元表达式吧。
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src, length=16, show=True):
    """接收bytes或string类型输入转换成十六进制数并输出"""
    if isinstance(src, bytes):
        src = src.decode()  # bytes类型先要解码成string类型
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i + length])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length * 3
        results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results


def receive_from(connection):
    buffer = b""
    connection.settimeout(10)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break

            buffer += data
    except Exception as e:
        print('error ', e)
        pass

    return buffer


def request_handler(buffer):
    # perform packet modifications
    return buffer


def response_handler(buffer):
    # perform packet modifications
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))  # 连接远程主机

    if receive_first:  # 确定是否要先从服务器接收一段数据
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # remote_buffer = response_handler(remote_buffer)
            # client_socket.send(remote_buffer)
            # print("[==>] Sent to local.")

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("[<==] Received %d bytes from local." % len(local_buffer))
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[==>] Sent to local.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """创建和管理连接"""
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        print(e)
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        print("> Received incoming connection from %s:%d" % (addr[0], addr[1]))

        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host,
                  remote_port, receive_first))
        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port,
                remote_host, remote_port, receive_first)


if __name__ == '__main__':
    main()
