import pywifi
import sys
import time
from pywifi import const
import socket

def connect():
    wifi=pywifi.PyWiFi()#创建一个无限对象
    ifaces=wifi.interfaces()[0]
    print(ifaces.name())

    # profile=pywifi.Profile()
    # profile.ssid='arduino'
    # profile.auth=const.AUTH_ALG_OPEN
    # profile.akm.append(const.AKM_TYPE_WPA2)
    # profile.cipher=const.CIPHER_TYPE_CCMP
    # profile.key='12345678'

    # ifaces.remove_all_network_profiles()#删除其他配置文件
    # tmp_profile=ifaces.add_network_profile(profile)#加载配置文件

    #ifaces.connect(tmp_profile)#连接
    #time.sleep(10)#尝试10秒能否成功连接
    isok=True

    if ifaces.status()==const.IFACE_CONNECTED:
       print("成功连接")
    else:
      print("失败")

def socket_client(ip,port):
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s_socket.listen()

    fail_count=0
    while(True):
        try:
            print("开始连接到服务器：\n")
            s_socket.connect((ip, port))
            break
        except socket.error:
            fail_count=fail_count+1
            print("连接服务器失败")
            if fail_count==10:
                return
    while(True):
        print("连接成功\n")
        s_buffer_send_size=s_socket.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
        s_buffer_reveive_size=s_socket.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
        print("client TCP send buffer size is %d" % s_buffer_send_size)
        print("client TCP receive buffer size is %d" % s_buffer_reveive_size)
        receive_count = 1
        while True:
            s=b'a\n'
            s_socket.send(s)
            # print("准备接受数据")
            # time.sleep(0.01)
            # msg = s_socket.recv(1024)
            # if(msg!=None):
            #     print(msg.decode('utf-8'))
            # else:
            #     continue


        s_socket.close()





if __name__ == '__main__':
    connect()
    socket_client('192.168.137.60', 100)