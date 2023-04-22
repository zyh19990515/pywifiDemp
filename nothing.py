import cv2
import socket
import time
ip='192.168.137.238'
port = 82
address_s = (ip, port)

s_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#s_socket.bind(address_s)
fail_count=0
while(True):
    try:
        print("开始连接到服务器：\n")
        s_socket.connect((ip,port))
        break
    except socket.error:
        fail_count=fail_count+1
        print("连接服务器失败")

while(True):
    # print("连接成功\n")
    # s_buffer_send_size=s_socket.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
    # s_buffer_reveive_size=s_socket.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
    # print("client TCP send buffer size is %d" % s_buffer_send_size)
    # print("client TCP receive buffer size is %d" % s_buffer_reveive_size)
    # receive_count = 1
    while True:

        s=b'everything will be ok\n'
        s_socket.send(s)
        print('success')
        time.sleep(2)
            # print("准备接受数据")
            # time.sleep(0.01)
            # msg = s_socket.recv(1024)
            # if(msg!=None):
            #     print(msg.decode('utf-8'))
            # else:
            #     continue
    s_socket.close()