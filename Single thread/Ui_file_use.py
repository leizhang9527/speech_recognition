# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work-space\eric6\python3_learn\learn0417\file_use.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(598, 459)
        font = QtGui.QFont()
        font.setFamily("华文宋体")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        MainWindow.setFont(font)
        MainWindow.setTabletTracking(True)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(460, 90, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 190, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 290, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(40, 30, 371, 361))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 598, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menuBar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menuBar)
        self.actiondakai = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/source/icon/Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiondakai.setIcon(icon)
        self.actiondakai.setObjectName("actiondakai")
        self.actiongunabi = QtWidgets.QAction(MainWindow)
        self.actiongunabi.setObjectName("actiongunabi")
        self.actionbaocun = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ico/source/icon/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbaocun.setIcon(icon1)
        self.actionbaocun.setObjectName("actionbaocun")
        self.help = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ico/source/icon/contact.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help.setIcon(icon2)
        self.help.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.help.setIconVisibleInMenu(True)
        self.help.setObjectName("help")
        self.actionA = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/ico/source/icon/About.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionA.setIcon(icon3)
        self.actionA.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.actionA.setMenuRole(QtWidgets.QAction.QuitRole)
        self.actionA.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionA.setObjectName("actionA")
        self.menu.addAction(self.actiondakai)
        self.menu.addAction(self.actionbaocun)
        self.menu_2.addAction(self.help)
        self.menu_3.addAction(self.actionA)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "开始录音"))
        self.pushButton_2.setText(_translate("MainWindow", "播放录音"))
        self.pushButton_3.setText(_translate("MainWindow", "语音识别"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华文宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.menu_3.setTitle(_translate("MainWindow", "关于"))
        self.actiondakai.setText(_translate("MainWindow", "打开"))
        self.actiondakai.setIconText(_translate("MainWindow", "open"))
        self.actiongunabi.setText(_translate("MainWindow", "gunabi"))
        self.actionbaocun.setText(_translate("MainWindow", "保存"))
        self.actionbaocun.setIconText(_translate("MainWindow", "save"))
        self.help.setText(_translate("MainWindow", "联系我们"))
        self.help.setIconText(_translate("MainWindow", "contact"))
        self.help.setToolTip(_translate("MainWindow", "help"))
        self.actionA.setText(_translate("MainWindow", "About"))

import my_pic_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

