#!/usr/bin/env python

import socket

addr = ('127.0.0.1', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 为 sock 打开地址可重用选项
sock.bind(addr)  # 绑定服务器地址
sock.listen(100)  # 设置监听队列

# 定义 "响应报文"
template = '''
HTTP/1.1 200 OK

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />

        <title>Seamile</title>

        <style>
            h1, p {
                text-align: center;
                font-size: 2.5em;
            }
            .avatar {
                border-radius: 20px;
                box-shadow: 5px 5px 20px grey;
                width: 500px;
                margin: 0 auto;
                display: block;
            }
        </style>
    </head>
    <body>
        <h1>Seamile</h1>
        <div><img class="avatar" src="https://inews.gtimg.com/newsapp_ls/0/10229330043_294195/0" /></div>
        <p>%s</p>
    </body>
</html>
'''


def get_url(request_str):
    '''从 "请求报文" 中获取请求的 URL'''
    first_line = request_str.split('\n')[0]  # 取出第一行
    url = first_line.split(' ')[1]  # 按空格切分，取出中间的 URL
    return url


while True:
    print('服务器已运行，正在等待客户端连接。。。')

    # 等待接受客户端连接
    # 第一个返回值是客户端的 socket 对象
    # 第二个返回值是客户端的地址
    cli_sock, cli_addr = sock.accept()
    print('接收到来自客户端 %s:%s 的连接' % cli_addr)

    # 接收客户端传来的数据，1024是接收缓冲区的大小
    cli_request = cli_sock.recv(1024).decode('utf8')
    print('接收到客户端发来的 "请求报文": \n%s' % cli_request)

    # 获取用户的 URL
    url = get_url(cli_request)

    # 根据 URL 生成不同的返回值
    if url == '/foo':
        response = template % '爱妃退下，朕在调戏代码'
    elif url == '/bar':
        response = template % '姜伟老师没醉过，但求一醉'
    else:
        response = template % 'hello world'

    print(url, response)
    cli_sock.sendall(response.encode('utf8'))  # 向客户端发送数据

    # 断开与客户端的连接
    cli_sock.close()
    print('连接断开, 退出！')
