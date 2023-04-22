import sys
import time
import cv2
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication,QDesktopWidget,QFrame,QGridLayout,QLabel,QHBoxLayout,
                             QTextEdit,QVBoxLayout)
import pyqtgraph as pg
from PyQt5.QtGui import QTextCursor, QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal,QObject, Qt
from PyQt5.QtCore import QSocketNotifier
import pywifi
import socket
import numpy as np
import time
#wifi线程

class QThread_video(QThread):
    signal_img = pyqtSignal(np.ndarray)
    signal_str = pyqtSignal(str)
    def __init__(self):
        super(QThread_video, self).__init__()
        self.url = 'http://192.168.137.156:81/stream'
        self.work = True

    def __del__(self):
        self.work = False
        self.wait()
    def run(self) -> None:
        self.video = cv2.VideoCapture(self.url)
        while self.work:
            self.success, self.img = self.video.read()
            if not self.success:
                continue
            #print(self.success)
            self.success = str(self.success)
            self.signal_str.emit(self.success)
            self.signal_img.emit(self.img)
            #print(self.img)





class QThread_control(QThread):
    def __init__(self, state):#state_d_t为转向或平移状态，state是转向中左转右转，或平移中前后左右状态
        super(QThread_control, self).__init__()
        #self.working=True
        self.working = True  # 工作状态
        self.wifi_working = True  # wifi连接状态
        self.state=state
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = '192.168.137.156'
        self.port = 100
        sock.connect((self.ip, self.port))
    def __del__(self):
        #self.working=False
        self.wait()
    def run(self):

        if (self.state == 'W'):
            #前
            sock.send(b'W\n')
            print('w')
            sock.close()
            time.sleep(0.01)
        elif(self.state == 'S'):
            sock.send(b'S\n')
            print('s')
            sock.close()
            time.sleep(0.01)
        elif (self.state == 'A'):
            sock.send(b'A\n')
            print("a")
            sock.close()
            time.sleep(0.01)
        elif (self.state == 'D'):
            sock.send(b'D\n')
            print('d')
            sock.close()
            time.sleep(0.01)
        elif(self.state == 'C'):
            sock.send(b'C\n')
            print('c')
            sock.close()
            time.sleep(0.01)



class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.IniteUI()    #UI布局
        self.control_button()
        self.DataOutput()
        self.thread_video = QThread_video()

        #self.wifi_connect()
    def IniteUI(self):
        self.setGeometry(0, 0, 1800, 1200)
        self.center()
        self.setWindowTitle("控制器")
        self.gridLayout=QGridLayout(self)

        self.frame_data=QFrame(self)
        self.frame_data.setFrameShape(QFrame.Panel)  # 设置父容器的面板形式
        self.frame_data.setFrameShadow(QFrame.Plain)  # 设置父容器边框阴影。
        self.frame_data.setLineWidth(2)  # 设置父容器边框线宽
        self.frame_data.setStyleSheet("background-color:rgb(255,255,255);")  # 设置表单颜色
        #创建一个父容器，放置控制按钮
        self.frame_control=QFrame(self)
        self.frame_control.setFrameShape(QFrame.Panel)  # 设置父容器的面板形式
        self.frame_control.setFrameShadow(QFrame.Plain)  # 设置父容器边框阴影。
        self.frame_control.setLineWidth(2)  # 设置父容器边框线宽
        self.frame_control.setStyleSheet("background-color:rgb(200,200,200);")  # 设置表单颜色
        self.label = QLabel(self)

        #创建视频播放窗口



        #初始化连接wifi按钮
        self.button_connect=QPushButton('连接', self)
        self.button_connect.clicked.connect(self.video_Thread)
        #self.button_connect.clicked.connect(self.wifi_connect)
        #self.button_disconnect = QPushButton('断开', self)
        #self.button_disconnect.clicked.connect(self.end)
        #布局
        self.gridLayout.addWidget(self.frame_data, 0, 0, 3, 5)
        self.gridLayout.addWidget(self.frame_control, 0, 3, 3, 5)
        #self.gridLayout.addWidget(self.button_connect, 6, 1, 1, 1)
        #self.gridLayout.addWidget(self.button_disconnect, 6, 2, 1, 1)


    def video_Thread(self):

        self.thread_video.start()
        self.thread_video.signal_img.connect(self.show_video)
        self.thread_video.signal_str.connect(self.showData)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def DataOutput(self):
        data_layout = QVBoxLayout(self.frame_data)  # 竖直放置
        self.picturelable = QLabel()
        #init_image = QPixmap(img).scaled(600, 600)
        # self.picturelable.setPixmap(init_image)
        self.textedit = QTextEdit()
        data_layout.addWidget(self.picturelable)
        data_layout.addWidget(self.textedit)

    def show_video(self, img):

        try:
            qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            #img_video = QPixmap(qimg).scaled(200, 200)

            self.picturelable.setPixmap(QPixmap.fromImage(qimg))

        except Exception as e:
            print(e)

    def showData(self, string):
        #print(string)
        self.textedit.setText(string)
        self.textedit.moveCursor(QTextCursor.End)

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

        self.button_zero = QPushButton('归零', self)
        self.button_zero.clicked.connect(self.move_zero)

        self.button_layout.addWidget(self.button_forward, 0, 1, 1, 1)
        self.button_layout.addWidget(self.button_back, 2, 1, 1, 1)
        self.button_layout.addWidget(self.button_left, 1, 0, 1, 1)
        self.button_layout.addWidget(self.button_right, 1, 2, 1, 1)
        self.button_layout.addWidget(self.button_zero, 1, 1, 1, 1)

    def KeyPressEvent(self, event):
        key = event.key()
        if(key == Qt.Key_Up):
            self.move_forward()
        elif(key == Qt.Key_Down):
            self.move_back()
        elif(key == Qt.Key_Left):
            self.move_left()
        elif(key == Qt.Key_Right):
            self.move_right()

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

    def move_zero(self):
        self.thread_control = QThread_control('C')
        self.thread_control.start()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
