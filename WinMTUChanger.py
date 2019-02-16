# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from subprocess import getoutput
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(210, 230)
        Dialog.setWindowIcon(QIcon('icon.ico'))

        # Initialize Variables
        self.mtu = 1500
        self.persistent = False

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 600, 461, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 160, 191, 16))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # Persistent CheckBox
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_5)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_5.addWidget(self.checkBox)
        self.checkBox.toggle()
        self.checkBox.clicked.connect(self.changePersistent)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(9, 9, 191, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)

        self.currentValue = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.currentValue.setEnabled(False)
        self.currentValue.setObjectName("currentValue")

        self.horizontalLayout_2.addWidget(self.currentValue)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 50, 191, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)

        # newValue
        self.newValue = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.newValue.setEnabled(True)
        self.newValue.setObjectName("newValue")
        self.horizontalLayout_3.addWidget(self.newValue)
        self.newValue.setText('400')

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 191, 21))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(13, 200, 181, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        
        self.applyButton = QtWidgets.QPushButton(Dialog)
        self.applyButton.setGeometry(QtCore.QRect(10, 90, 93, 61))
        self.applyButton.setAutoRepeatDelay(300)
        self.applyButton.setObjectName("applyButton")
        self.applyButton.clicked.connect(self.changeReg)
        
        self.initButton = QtWidgets.QPushButton(Dialog)
        self.initButton.setGeometry(QtCore.QRect(110, 90, 93, 61))
        self.initButton.setObjectName("initButton")
        self.initButton.clicked.connect(self.initMtu)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "WMTUC"))
        self.checkBox.setText(_translate("Dialog", "영구 적용  활성화"))
        self.label.setText(_translate("Dialog", "현재값 : "))
        self.label_2.setText(_translate("Dialog", "변경값 : "))
        self.label_3.setText(_translate("Dialog", "WinMTUChanger (v1.0)"))
        self.label_4.setText(_translate("Dialog", "whackur@gmail.com"))
        self.applyButton.setText(_translate("Dialog", "적용"))
        self.initButton.setText(_translate("Dialog", "초기화"))
    
    def getIfNum(self):
        batcmd = 'powershell.exe \"Get-WMIObject Win32_networkadapter | Select-Object InterfaceIndex\"'
        r = getoutput(batcmd)
        r = r.split('\n') # split by line
        r2 = []
        r3 = []

        for i in r:
            for repeat in range(10):
                j = i.replace(' ','')
            r2.append(j)

        for i in r2:
            if i.isnumeric():
                r3.append(i)
        return r3
        
    def changeReg(self):
        self.mtu = self.newValue.text()
        ifNums = self.getIfNum()
        self.currentValue.setText(self.mtu) # For Display Current Value
        for ifNum in ifNums:
            if self.persistent == True:
                print('netsh interface ipv4 set subinterface %s mtu=%s store=persistent' %(ifNum, self.mtu))
                os.system('netsh interface ipv4 set subinterface %s mtu=%s store=persistent' %(ifNum, self.mtu))
            else:
                print('netsh interface ipv4 set subinterface %s mtu=%s' %(ifNum, self.mtu))
                os.system('netsh interface ipv4 set subinterface %s mtu=%s' %(ifNum, self.mtu))
    
    def initMtu(self):
        self.newValue.setText("1500")
        self.mtu = 1500
        self.persistent = True
        self.changeReg()

    def changePersistent(self):
        if self.checkBox.isChecked():
            self.persistent = True
            print(self.persistent)
        else:
            self.persistent = False
            print(self.persistent)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())