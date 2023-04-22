import sys
import time

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication,QDesktopWidget,QFrame,QGridLayout,QLabel,QHBoxLayout,
                             QTextEdit,QVBoxLayout)
#import pyqtgraph as pg
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtCore import QSocketNotifier
#import pywifi
import socket
#from pywifi import const
#from wificlass import wifi_control
#wifi线程

class QThread_wifi(QThread):
    output = pyqtSignal(str)
    def __init__(self):
        super(QThread_wifi, self).__init__()
        self.working=True   #工作状态
        self.wifi_working=True  #wifi连接状态
        #self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #global s_socket
        #s_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #self.connect()

        #self.receive()
        #self.ip = '192.168.137.214'
        self.ip = '192.168.137.101'
        self.port = 100
    def __del__(self):
        self.working=False
        #self.wait()
    def run(self):
        #self.connect()
        #self.send(bytes('data'))
        # wifi = pywifi.PyWiFi()  # 创建一个无限对象
        # ifaces = wifi.interfaces()[0]
        # print(ifaces.name())
        # if ifaces.status() == const.IFACE_CONNECTED:
        #     print("成功连接\n")
        #     str="成功连接\n"
        #     self.output.emit(str)
        # else:
        #     print("失败")
        fail_count = 0
        while (True):
            try:
                print("开始连接到服务器：\n")
                str = '开始连接到服务器：'
                # self.output.emit(str)
                #self.s_socket.connect(('192.168.4.1', 80))
                sock.connect((self.ip, self.port))
                # s_socket.connect(('192.168.4.1', 80))
                print("...")
                break
            except socket.error:
                fail_count = fail_count + 1
                print("连接服务器失败")
                if fail_count == 100:
                    return




class QThread_control(QThread):
    def __init__(self, state):#state_d_t为转向或平移状态，state是转向中左转右转，或平移中前后左右状态
        super(QThread_control, self).__init__()
        #self.working=True
        self.state=state
    def __del__(self):
        #self.working=False
        self.wait()
    def run(self):

        if (self.state == 'W'):
            #前
            sock.send(b'WW\n')
            print("1")
            time.sleep(0.1)
        elif(self.state == 'S'):
            sock.send(b'SS\n')
            print("1")
            time.sleep(0.1)
        elif (self.state == 'A'):
            sock.send(b'AA\n')
            print("1")
            time.sleep(0.1)
        elif (self.state == 'D'):
            sock.send(b'DD\n')
            print("1")
            time.sleep(0.1)

class QThread_video(QThread):
    def __init__(self):
        super(QThread_video, self).__init__()


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.IniteUI()    #UI布局
        self.control_button()
        self.thread=QThread_wifi()
        self.DataOutput()

        # self.wifi_connect()
    def IniteUI(self):
        self.setGeometry(0, 0, 1800, 1200)
        # self.center()
        self.setWindowTitle("控制器")
        self.gridLayout = QGridLayout(self)

        self.frame_data = QFrame(self)
        self.frame_data.setFrameShape(QFrame.Panel)  # 设置父容器的面板形式
        self.frame_data.setFrameShadow(QFrame.Plain)  # 设置父容器边框阴影。
        self.frame_data.setLineWidth(2)  # 设置父容器边框线宽
        self.frame_data.setStyleSheet("background-color:rgb(255,255,255);")  # 设置表单颜色
        # 创建一个父容器，放置控制按钮
        self.frame_control = QFrame(self)
        self.frame_control.setFrameShape(QFrame.Panel)  # 设置父容器的面板形式
        self.frame_control.setFrameShadow(QFrame.Plain)  # 设置父容器边框阴影。
        self.frame_control.setLineWidth(2)  # 设置父容器边框线宽
        self.frame_control.setStyleSheet("background-color:rgb(200,200,200);")  # 设置表单颜色
        self.label = QLabel(self)
        # 初始化连接wifi按钮
        self.button_connect = QPushButton('连接', self)
        self.button_connect.clicked.connect(self.start)
        # self.button_connect.clicked.connect(self.wifi_connect)
        self.button_disconnect = QPushButton('断开', self)
        self.button_disconnect.clicked.connect(self.end)
        # 布局
        self.gridLayout.addWidget(self.frame_data, 0, 0, 3, 5)
        self.gridLayout.addWidget(self.frame_control, 0, 3, 3, 5)
        self.gridLayout.addWidget(self.button_connect, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.button_disconnect, 6, 2, 1, 1)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def DataOutput(self):
        text_layout = QVBoxLayout(self.frame_data)  # 竖直放置

        self.textedit = QTextEdit()
        text_layout.addWidget(self.textedit)
    def showData(self, str):
        self.textedit.setText(str)

    def control_button(self):
        self.button_layout = QGridLayout(self.frame_control)
        self.button_forward = QPushButton('前', self)
        self.button_forward.clicked.connect(self.move_forward)

        self.button_back = QPushButton('后', self)
        self.button_back.clicked.connect(self.move_back)

        self.button_left = QPushButton('左', self)
        self.button_left.clicked.connect(self.move_left)

        self.button_right = QPushButton('右', self)
        self.button_right.clicked.connect(self.move_right)
        self.button_layout.addWidget(self.button_forward, 0, 1, 1, 1)
        self.button_layout.addWidget(self.button_back, 2, 1, 1, 1)
        self.button_layout.addWidget(self.button_left, 1, 0, 1, 1)
        self.button_layout.addWidget(self.button_right, 1, 2, 1, 1)

    def start(self):
        self.thread.start()
        self.thread.output.connect(self.showData)
    def end(self):
        self.thread.working=False

    def move_forward(self):
        self.thread_control = QThread_control('W')
        self.thread_control.start()

    def move_back(self):
        self.thread_control = QThread_control('S')
        self.thread_control.start()

    def move_left(self):
        self.thread_control = QThread_control('A')
        self.thread_control.start()

    def move_right(self):
        self.thread_control = QThread_control('D')
        self.thread_control.start()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())