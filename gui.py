from PyQt5 import QtWidgets, uic, QtCore, QtGui
import os

path = os.getcwd()
qtCreatorFile = path + os.sep + "ui" + os.sep + "SL_manage.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
# 这个主要用于后期的UI界面文字字体以及颜色便捷的更改
_translate = QtCore.QCoreApplication.translate


# 创建一个对象，该对象就是你的整个窗体：
class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):
    # 这里的第一个变量是你该窗口的类型，第二个是该窗口对象。
    # 这里是主窗口类型。所以设置成当QtWidgets.QMainWindow。
    # 你的窗口是一个会话框时你需要设置成:QtWidgets.QDialog
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
