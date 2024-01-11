# -*- coding: utf-8 -*-
#-*- author: Wale Yu              -*-
#-*- update: 2023.5.21              -*-
#-*- email:  chuanqi_yu2021@126.com -*-

from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1500, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(1500, 800))
        Form.setMaximumSize(QtCore.QSize(1500, 800))
        Form.setStyleSheet(
    """
        QPushButton {
            background-color: lightblue;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 16px;
            color: black;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: lightgreen;
        }

        QPushButton:pressed {
            background-color: rgb(85, 170, 255);
            border-style: inset;
        }
        QLabel{
            background-color: lightblue;
            border-radius: 5px;
        }
        QLineEdit{
            background-color: lightgreen;
            border-radius: 5px;
        }
        """)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(1290, 9, 201, 350))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout.setStretch(1, 6)
        self.verticalLayout.setStretch(2, 5)
        self.verticalLayout.setStretch(3, 5)
        self.verticalLayout.setStretch(4, 5)
        self.handleButton = QtWidgets.QPushButton(Form)
        self.handleButton.setGeometry(QtCore.QRect(1290, 460, 201, 61))
        self.handleButton.setObjectName("handleButton")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(740, 760, 750, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(740, 730, 491, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(1230, 730, 41, 21))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 720, 201, 81))
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(1300, 730, 101, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(1400, 730, 51, 20))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(1450, 730, 41, 20))
        self.label_8.setObjectName("label_8")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(360, 720, 211, 81))
        self.label_12.setObjectName("label_12")
        self.lineEdit = QtWidgets.QLabel(Form)
        self.lineEdit.setGeometry(QtCore.QRect(220, 750, 51, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLabel(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(290, 750, 51, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLabel(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(590, 750, 51, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLabel(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(660, 750, 51, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(1290, 540, 196, 181))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.lineEdit_5, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout.addWidget(self.lineEdit_6, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout.addWidget(self.lineEdit_7, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout.addWidget(self.lineEdit_8, 3, 1, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "WTG-Risk-Control"))
        self.groupBox.setTitle(_translate("Form", "Select ROI"))
        self.pushButton.setToolTip(_translate("Form", "选取方形区域"))
        self.pushButton.setText(_translate("Form", "\n"
"Rectangle\n"
""))
        self.pushButton_2.setToolTip(_translate("Form", "设置准确坐标"))
        self.pushButton_2.setText(_translate("Form", "\n"
"Position\n"
""))
        self.pushButton_4.setToolTip(_translate("Form", "清除所有"))
        self.pushButton_4.setText(_translate("Form", "\n"
"Clear all\n"
""))
        self.pushButton_5.setToolTip(_translate("Form", "确认"))
        self.pushButton_5.setText(_translate("Form", "\n"
"Confirm\n"
""))
        self.handleButton.setText(_translate("Form", "\n"
"Handle\n"
""))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:8pt;\">The current number of feature points matched in the frame:</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:8pt;\">00</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:8pt;\">The coordinates of the </span></p><p><span style=\" font-size:8pt;\">upper left corner of </span></p><p><span style=\" font-size:8pt;\">the selected graphic:</span></p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:8pt;\">Frame Rate：</span></p></body></html>"))
        self.label_6.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:8pt;\">00</span></p></body></html>"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:8pt;\">fps</span></p></body></html>"))
        self.label_12.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:8pt;\">The length and width </span></p><p><span style=\" font-size:8pt;\">of the selected graphic:</span></p></body></html>"))
        self.label_7.setText(_translate("Form", "FrameNumber"))
        self.label_9.setText(_translate("Form", "Time"))
        self.label_10.setText(_translate("Form", "avg_u"))
        self.label_11.setText(_translate("Form", "avg_v"))
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setContentsMargins(3, 5, 3, 3)
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 3, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 4)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "SOI"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.groupBox.setTitle(_translate("Dialog", "SOI"))