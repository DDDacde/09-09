#!/usr/bin/env python

import socket
import time

addr = ('127.0.0.1', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 为 sock 打开地址可重用选项
sock.bind(addr)  # 绑定服务器地址
sock.listen(100)  # 设置监听队列

# 定义 "响应报文"
html = b'''
HTTP/1.1 200 OK

<html>
    <head>
        <title>home</title>
    </head>
    <body>,b n ,
        Hello world
    </body>
</html>
'''

while True:
    print('服务器已运行，正在等待客户端连接。。。')

    # 等待接受客户端连接
    # 第一个返回值是客户端的 socket 对象
    # 第二个返回值是客户端的地址
    cli_sock, cli_addr = sock.accept()
    print('接收到来自客户端 %s:%s 的连接' % cli_addr)

    # 接收客户端传来的数据，1024是接收缓冲区的大小
    cli_data = cli_sock.recv(1024)
    print('接收到客户端发来的 "请求报文": \n%s' % cli_data.decode('utf8'))

    cli_sock.sendall(html)  # 向客户端发送数据

    # 断开与客户端的连接
    cli_sock.close()
    print('连接断开, 退出！')
