import sys
from PyQt5.QtWidgets import (QWidget,QApplication,QPushButton,QToolTip,QMessageBox,QDesktopWidget,QLabel,QVBoxLayout,
                             QHBoxLayout,QGridLayout)
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLCDNumber,QSlider
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
#############################################
#示例1
#############################################

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = QWidget()
#     w.resize(1300,900)
#     w.move(0,0)
#     w.setWindowTitle('test')
#     w.show()
#
#     sys.exit(app.exec_())

class example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # bth=QPushButton('quit',self)
        # bth.setToolTip('This is a quit button')
        # bth.clicked.connect(QCoreApplication.instance().quit)
        # bth.resize((bth.sizeHint()))
        # bth.move(30,30)
        #
        # lbl1=QLabel('1',self)
        # lbl1.move(10,15)
        #
        # lbl2 = QLabel('2', self)
        # lbl2.move(60, 75)

        #############################################
        # 两个横向布局的按钮
        #############################################
        # okbutton=QPushButton('ok')
        # okbutton.clicked.connect(QCoreApplication.instance().quit)
        # cancelbutton=QPushButton('cancel')
        # hbox=QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(okbutton)
        # hbox.addWidget(cancelbutton)
        # vbox=QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)
        # self.setLayout(vbox)

        #############################################
        # 网格布局按钮
        #############################################

        # grid=QGridLayout()
        # self.setLayout(grid)
        # names = ['Cls', 'Bck', '', 'Close',
        #          '7', '8', '9', '/',
        #          '4', '5', '6', '*',
        #          '1', '2', '3', '-',
        #          '0', '.', '=', '+']
        #
        # positions=[(i,j) for i in range(5) for j in range(4)]
        # for position,name in zip(positions,names):
        #     if names=='':
        #         continue
        #     button=QPushButton(name)
        #     grid.addWidget(button,*position)

        #############################################
        # 信号事件
        #############################################
        # lcd=QLCDNumber(self)
        # sld=QSlider(Qt.Horizontal,self)
        # vbox=QVBoxLayout()
        # vbox.addWidget(lcd)
        # vbox.addWidget(sld)
        # self.setLayout(vbox)
        # sld.valueChanged.connect(lcd.display)

        #############################################
        # 重新实现事件处理器
        #############################################
        button1=QPushButton('button1',self)
        button1.move(30,30)
        button2=QPushButton('button2',self)
        button2.move(150,150)





        self.setGeometry(300,300,1150,800)
        self.center()
        self.setWindowTitle('test')
        self.show()




    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=example()
    sys.exit(app.exec_())