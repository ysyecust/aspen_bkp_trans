import re
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class ComboxDemo(QWidget):
    def __init__(self):
        super().__init__()
        # 设置标题
        self.num = 0
        self.setWindowTitle('ASPEN版本转化工具')
        # 设置初始界面大小
        self.resize(500, 300)
        # 实例化QComBox对象 
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 100, 100, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("打开文件")
        self.pushButton.clicked.connect(self.openfile)
        self.cb = QComboBox(self)
        self.cb.setGeometry(QtCore.QRect(100, 100, 100, 40))
        # self.cb.move(250, 150)
        # 单个添加条目
   
        self.cb.addItem('V9')
        self.cb.addItem('V10')
        self.cb.addItem('V11')
        self.cb.addItem('V12')
        self.item = ['V9','V10','V11','V12']

        # 信号
        self.cb.currentIndexChanged[str].connect(self.print_value) # 条目发生改变，发射信号，传递条目内容
        self.cb.currentIndexChanged[int].connect(self.print_value)  # 条目发生改变，发射信号，传递条目索引
        self.cb.highlighted[str].connect(self.print_value)  # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目内容
        self.cb.highlighted[int].connect(self.print_value)  # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目索引
        QtCore.QMetaObject.connectSlotsByName(self)

    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','bkp files(*.bkp)')
        print(openfile_name[0])
        try:
            self.read_file(openfile_name[0],self.version)
        except:
            pass
    def print_value(self, i):
        self.version = i
    def read_file(self,file_path,target_version):
        print(target_version)
        with open(file_path, 'rb') as f:
            filename = file_path.split("\\")
            new_name = filename[-1].split(".")[0]+target_version+".bkp"
            # MMSUMMARY38.0
            # MMSUMMARY38.0
            print(new_name)
            file_content = f.read()
            content = file_content.decode('utf-8', 'ignore')
            x = content.find("MMSUMMARY")
        
            version_num = "V"+str(int(content[x+9:x+11])-26)
            print("此bkp文件是aspen{}版本创建".format(version_num))
            data = {"V9":{"APV":"APV90","Version":"\"35.0\"","PURE":"PURE35"},
                    "V10":{"APV":"APV100","Version":"\"36.0\"","PURE":"PURE36"},
                    "V11":{"APV":"APV110","Version":"\"37.0\"","PURE":"PURE37"},
                    "V12":{"APV":"APV120","Version":"\"38.0\"","PURE":"PURE38"},
                    }
            new_content = re.sub(data[version_num]["Version"], data[target_version]["Version"],content)
            new_content = re.sub(data[version_num]["APV"], data[target_version]["APV"],new_content)
            new_content = re.sub(data[version_num]["PURE"], data[target_version]["PURE"],new_content)
            

            fo = open(new_name,"w",encoding='utf-8')
            fo.write(new_content)
            print("已生成aspen{}版本bkp文件".format(target_version))


if __name__ == '__main__':
    global num
    app = QApplication(sys.argv)
    comboxDemo = ComboxDemo()
    comboxDemo.show()
    sys.exit(app.exec_())