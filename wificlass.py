import pywifi
from pywifi import const
import socket

class wifi_control():
    def __init__(self):
        super(wifi_control, self).__init__()
        #self.ip = '192.168.4.1'
        #self.port = 80
        #self.connect()
        #self.control()
        self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.up()
        # self.down()
        # self.left()
        # self.right()
    def connect(self):
        wifi = pywifi.PyWiFi()  # 创建一个无限对象
        ifaces = wifi.interfaces()[0]
        print(ifaces.name())
        if ifaces.status() == const.IFACE_CONNECTED:
            print("成功连接")
        else:
            print("失败")

        #self.s_socket.listen(5)
    def control(self):
        fail_count = 0

        while (True):
            try:
                print("开始连接到服务器：\n")
                self.s_socket.connect(('192.168.137.112', 100))
                break
            except socket.error:
                fail_count = fail_count + 1
                print("连接服务器失败")
                if fail_count == 100:
                    return
    def getdata(self):
        #给服务器发送0，服务器接收后发送数据
        state = b'0'
        self.s_socket.sendall(state)
        print("ready to get data")
        data = self.s_socket.recv(1024)
        print(data.decode("utf-8"))

if __name__ == '__main__':
    wifi = wifi_control()
    wifi.connect()
    wifi.control()
    wifi.getdata()