# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 480)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 3, 2)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(2, 2)
        self.gridLayout.setRowStretch(3, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About WTG-Risk-Control"))
        self.pushButton.setText(_translate("Dialog", "Close"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">WTG-Risk-Control</span></p><p><br/></p><p><span style=\" font-size:8pt;\">Version: v 1.1.0</span></p><p><span style=\" font-size:8pt;\">WTG-Risk-Control is a software used for monitoring and analyzing wind </span></p><p><span style=\" font-size:8pt;\">turbine tower damage detection.</span></p><p><span style=\" font-size:8pt;\">The programming language used for WTG-Risk-Control is Python,and the</span></p><p><span style=\" font-size:8pt;\">interface is developed based on the PyQt5 framework.The image processing</span></p><p><span style=\" font-size:8pt;\">is carried out using OpenCV library.</span></p><p><span style=\" font-size:8pt;\">WTG-Risk-Control was developed by Huangxingjian,Yuchuanqi and Pengjunming.</span></p><p><span style=\" font-size:8pt;\">Yuchuanqi was responsible for interface design and software</span></p><p><span style=\" font-size:8pt;\">production,while Huangxingjian and Pengjunming were responsible for </span></p><p><span style=\" font-size:8pt;\">the calculation and logical processing.</span></p><p><br/></p><p><span style=\" font-size:10pt; font-weight:600;\">Thank you for using WTG-Risk-Control!</span></p><p><span style=\" font-size:10pt; font-weight:600;\">We hope you can provide valuable feedback for improvement!</span></p><p><span style=\" font-size:10pt; font-weight:600;\">Email:Xingjian_Huang@outlook.com,chuanqi_yu2021@126.com</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
