# Form implementation generated from reading ui file 'Python_Chat_2.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(404, 667)
        MainWindow.setMinimumSize(QtCore.QSize(404, 667))
        MainWindow.setMaximumSize(QtCore.QSize(404, 667))
        MainWindow.setStyleSheet("QWidget {\n"
"    color: white;\n"
"    background-color: #00FFFF;\n"
"    fonf-family: Roboto;\n"
"    font-size: 12pt;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: black;\n"
"    border:     2px solid yellow;\n"
"    border-radius: 10%;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #888;\n"
"}\n"
"\n"
"QTextBrowser {\n"
"    color: black;\n"
"    background-color: white;\n"
"    border:     2px solid yellow;\n"
"}\n"
"\n"
"QTextEdit {\n"
"    color: black;\n"
"    background-color: white;\n"
"    border:     2px solid yellow;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #000000;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_login = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_login.sizePolicy().hasHeightForWidth())
        self.label_login.setSizePolicy(sizePolicy)
        self.label_login.setObjectName("label_login")
        self.horizontalLayout.addWidget(self.label_login)
        self.label_login_name = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_login_name.setEnabled(False)
        self.label_login_name.setText("")
        self.label_login_name.setObjectName("label_login_name")
        self.horizontalLayout.addWidget(self.label_login_name)
        self.pushButton_logout = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_logout.sizePolicy().hasHeightForWidth())
        self.pushButton_logout.setSizePolicy(sizePolicy)
        self.pushButton_logout.setObjectName("pushButton_logout")
        self.horizontalLayout.addWidget(self.pushButton_logout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.textBrowser_output_message = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.textBrowser_output_message.setObjectName("textBrowser_output_message")
        self.verticalLayout_2.addWidget(self.textBrowser_output_message)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit_input_message = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit_input_message.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_input_message.sizePolicy().hasHeightForWidth())
        self.textEdit_input_message.setSizePolicy(sizePolicy)
        self.textEdit_input_message.setObjectName("textEdit_input_message")
        self.horizontalLayout_2.addWidget(self.textEdit_input_message)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_send = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_send.sizePolicy().hasHeightForWidth())
        self.pushButton_send.setSizePolicy(sizePolicy)
        self.pushButton_send.setObjectName("pushButton_send")
        self.verticalLayout.addWidget(self.pushButton_send)
        self.comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Chat"))
        self.label_login.setText(_translate("MainWindow", "Логін:"))
        self.pushButton_logout.setText(_translate("MainWindow", "Вийти"))
        self.pushButton_send.setText(_translate("MainWindow", "Відправити"))
