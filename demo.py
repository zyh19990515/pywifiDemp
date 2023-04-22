'''需要用到的库：
    UI:PyQt5,pyqtgraph
    蓝牙:pybluez
'''

import pyqtgraph as pg
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QGridLayout, QLabel, QVBoxLayout,
                             QPushButton, QHBoxLayout,QDesktopWidget)
from PyQt5.QtCore import Qt,QTimer
import bluetooth
import re
from bluetooth.btcommon import BluetoothError
import traceback


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUi()
        self.generate_image()
        self.encoder_A = []
        self.encoder_B = []
        self.encoder_C = []
        self.encoder_D = []
        self.angel_x = []
        self.angel_y = []

    #UI布局
    def InitUi(self):
        self.setGeometry(0,0,1800,1200)
        self.center()
        self.setWindowTitle("实时接收蓝牙数据")
        self.gridLayout = QGridLayout(self)
        # 创建一个父容器-波形
        self.frame_angel = QFrame(self)
        self.frame_angel.setFrameShape(QFrame.Panel)   #设置父容器的面板形式
        self.frame_angel.setFrameShadow(QFrame.Plain)  #设置父容器边框阴影。
        self.frame_angel.setLineWidth(2)               #设置父容器边框线宽
        self.frame_angel.setStyleSheet("background-color:rgb(0,255,255);")  #设置表单颜色
        # 创建一个父容器-数据
        self.frame_text = QFrame(self)
        self.frame_text.setFrameShape(QFrame.Panel)  # 设置父容器的面板形式
        self.frame_text.setFrameShadow(QFrame.Plain)  # 设置父容器边框阴影。
        self.frame_text.setLineWidth(2)  # 设置父容器边框线宽
        self.frame_text.setStyleSheet("background-color:rgb(255,255,255);")  # 设置表单颜色

        self.label = QLabel(self)
        self.label.setText("波形")
        self.button_connect = QPushButton('connect',self)
        self.button_getData = QPushButton('getData',self)
        self.button_connect.clicked.connect(self.bthInite)
        self.button_getData.clicked.connect(self.btnClick)
        self.gridLayout.addWidget(self.frame_angel,0,0,5,5)   #griflayout的使用，将frame容器放在grid得一行
        self.gridLayout.addWidget(self.frame_text, 0,5,5,3 )
        self.gridLayout.addWidget(self.label,5,0,1,1)   #将label和button，放在grid一行
        self.gridLayout.addWidget(self.button_connect,5,6,1,1)
        self.gridLayout.addWidget(self.button_getData,5,7,1,1)
        self.setLayout(self.gridLayout)
    #将窗口移至屏幕中间
    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    #产生波形图
    def generate_image(self):
        verticalLayout = QHBoxLayout(self.frame_angel)   #创建父容器后需要将graph添加到里面，采用QVBoxLaouth或者QHBoxLayout
        win = pg.GraphicsLayoutWidget(self.frame_angel)  #将其显示在frame上
        verticalLayout.addWidget(win)
        p = win.addPlot(title = "")
        p.showGrid(x=True,y=True)
        p.setLabel(axis="left",text ="angel")
        p.setLabel(axis="bottom",text="time")
        p.setTitle("Angel Data")
        p.addLegend()

        self.curve1 = p.plot(pen="r",name="angel_x")#x方向的角度数据图像
        self.curve2 = p.plot(pen='g',name="angel_y")#y方向的角度数据图像
    #蓝牙初始化
    def bthInite(self):
        print("Performing inquiry...")
        #搜索附近蓝牙设备并输出名字及地址信息
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
        print("Found {} devices".format(len(nearby_devices)))
        for addr, name in nearby_devices:
            try:
                print("   {} - {}".format(addr, name))
            except UnicodeEncodeError:
                print("   {} - {}".format(addr, name.encode("utf-8", "replace")))

        #在附近蓝牙设备中找到目标蓝牙，用sock方式连接，通讯协议为RFCOMM方式
        #程序运行之前确保电脑与蓝牙设备已经连接，否侧会报错
        for addr, name in nearby_devices:
            addr_target = ''
            if name == 'BT04-A':
                addr_target = addr
                print(addr)
                global sock
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                try:
                    sock.connect((addr_target, 1))
                    print("Connection successful. Now ready to get the data")
                    # count = 0
                    #
                    # while (1):
                    #     data = sock.recv(1024)
                    #     print(data)
                    #     data = data.decode('utf-8')
                    #     self.angel_x, self.angel_y = self.getData(data)
                    #     self.curve1.setData(self.angel_x)
                    #     self.curve1.setData(self.angel_y)
                    #     count += 1
                except BluetoothError as e:
                    print("fail\n")

    #用sock接受数据，包含编码器数据以及陀螺仪数据，并画图
    def plotData(self):
        try:
            data = sock.recv(1024)
            #print(data)
            data = data.decode('utf-8')
            self.angel_x, self.angel_y = self.getData(data)
            #画图
            self.curve1.setData(self.angel_x)
            self.curve2.setData(self.angel_y)
        except Exception as e:
            print(traceback.print_exc())

    #处理数据
    '''
       原始数据格式为：
       b'{A0:0:20:0}$'
       b'{B27:-9:10:0}$' 
    '''
    #A：编码器数据
    #B：陀螺仪数据
    def getData(self,data):
        if (data[1] == 'A'):
            data_re = re.findall("\d+", data)#用正则表达式找到数据中的数字部分，data_re得到包含4个数据的列表
            #将data_re中数据转为float性，分别放入对应列表
            self.encoder_A.append(float(data_re[0]))
            self.encoder_B.append(float(data_re[1]))
            self.encoder_C.append(float(data_re[2]))
            self.encoder_D.append(float(data_re[3]))
        else:
            data_re = re.findall("\d+", data)
            self.angel_x.append(float(data_re[0]))
            self.angel_y.append(float(data_re[1]))
            print("angel_x:",self.angel_x)
            print("angel_y:", self.angel_y)
            if(len(self.angel_x)>60):
                #self.angel_x = self.angel_x.remove(self.angel_x[0])
                del self.angel_x[0]
            else:
                self.angel_x = self.angel_x
            if (len(self.angel_y) > 60):
                #self.angel_y = self.angel_y.remove(self.angel_y[0])
                del self.angel_y[0]
            else:
                self.angel_y = self.angel_y

        return self.angel_x,self.angel_y

    #使用Timer方法刷新图像，实现数据实时表示
    def btnClick(self):
        self.button_getData.setText("pause")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.plotData)
        self.timer.start(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())