# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(556, 439)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("1.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setDocumentMode(True)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 360, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.textEdit = QtGui.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(50, 40, 451, 281))
        self.textEdit.setMouseTracking(True)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.setStyleSheet(_fromUtf8("background-color: rgb(246, 255, 221);"))
        self.textEdit.setLineWidth(0)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.pushButton_2 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 360, 93, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 360, 93, 28))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.textEdit.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "       语音识别", None))
        self.pushButton.setText(_translate("MainWindow", "开始录音", None))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.pushButton_2.setText(_translate("MainWindow", "停止录音", None))
        self.pushButton_3.setText(_translate("MainWindow", "清空内容", None))

