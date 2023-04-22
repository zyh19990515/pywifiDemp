import numpy as np
import pyqtgraph as pg
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QGridLayout, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt,QTimer

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUi()
        self.generate_image()

    def InitUi(self):
        self.setGeometry(200,200,1000,800)
        self.setWindowTitle("实时刷新波形实验")
        self.gridLayout = QGridLayout(self)
        self.frame = QFrame(self)      #创建一个父容器
        self.frame.setFrameShape(QFrame.Panel)   #设置父容器的面板形式
        self.frame.setFrameShadow(QFrame.Plain)  #设置父容器边框阴影。
        self.frame.setLineWidth(2)               #设置父容器边框线宽
        self.frame.setStyleSheet("background-color:rgb(0,255,255);")  #设置表单颜色
        self.label = QLabel(self)
        self.label.setText("波形")
        self.button = QPushButton('connect',self)
        self.button.clicked.connect(self.btnClick)
        self.gridLayout.addWidget(self.frame,0,0,1,2)   #griflayout的使用，将frame容器放在grid得一行
        self.gridLayout.addWidget(self.label,1,0,1,1)   #将label和button，放在grid一行
        self.gridLayout.addWidget(self.button,1,1,1,1)
        self.setLayout(self.gridLayout)

    def generate_image(self):
        verticalLayout = QHBoxLayout(self.frame)   #创建父容器后需要将graph添加到里面，采用QVBoxLaouth或者QHBoxLayout
        win = pg.GraphicsLayoutWidget(self.frame)  #将其显示在frame上
        verticalLayout.addWidget(win)
        p = win.addPlot(title = "")
        p.showGrid(x=True,y=True)
        p.setLabel(axis="left",text ="Y Value")
        p.setLabel(axis="bottom",text="X Value")
        p.setTitle("数据分析")
        p.addLegend()

        self.curve1 = p.plot(pen="r",name="y1")
        self.curve2 = p.plot(pen='g',name="y2")

        self.Fs = 1024.0 #采样频率
        self.N = 1024    #采样点数
        self.f0 = 4.0    #信号频率
        self.pha = 60     #初试相位

        self.t = np.arange(self.N) /self.Fs    #时间向量1*1024的矩阵
        print(self.t)
        print(np.arange(self.N))
    def plotData(self):
        self.pha += 90
        self.curve1.setData(self.t,6*np.sin(8*np.pi*self.t+self.pha*np.pi/180.0))
        self.curve2.setData(self.t,6*np.cos(8 * np.pi * self.t + self.pha * np.pi / 180.0))


    def btnClick(self):
        self.button.setText("再次点击退出")
        timer = QTimer(self)
        timer.timeout.connect(self.plotData)
        timer.start(100)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

