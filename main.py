import sys, sqlite3

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow
from sign_in import Ui_MainWindow as sign_in
from registration import Ui_MainWindow as registration
from Python_Chat import Ui_MainWindow as Python_Chat
from datetime import datetime

db = sqlite3.connect('handler/Python Chat.db')
cursor = db.cursor()

class Win_sign_in(QMainWindow, sign_in):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.pushButton_sign_in.clicked.connect(lambda: self.openDialog1(self.lineEdit_login.text(), self.lineEdit_password.text()))
        self.label_registration.mousePressEvent = self.openDialog2
        self.checkBox_show_password.stateChanged.connect(self.show_password)

        self.Registration = Win_registration()
        self.Python_Chat = Win_Python_Chat()

    def show_password(self, state):
        if (QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked):
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def openDialog1(self, login, password):
        cursor.execute(f"SELECT * FROM user WHERE login = '{login}' or email = '{login}'")
        data = cursor.fetchall()

        if data != [] and data[0][3] == password and login != []:
            print("Успешный вход")
            error = QMessageBox()
            error.setIcon(QMessageBox.Icon.Information)
            error.setText('Успешный вход')
            error.exec()
            self.Python_Chat.show()
            self.Python_Chat.label_login_name.setText(login)
            # Python_Chat().lineEdit_login_name.setText(login)
            self.hide()
        else:
            print("Не верные даные (Логин либо пароль)")
            error = QMessageBox()
            error.setIcon(QMessageBox.Icon.Information)
            error.setText('Не верные даные (Логин либо пароль)')
            error.exec()

    def openDialog2(self, event):
        self.Registration.show()
        self.hide()

    def openDialog3(self):
        self.show()

class Win_registration(QMainWindow, registration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_registration.clicked.connect(self.registration)
        self.checkBox_show_password.stateChanged.connect(self.show_password)
        self.label_sign_in.mousePressEvent = self.openDialog2

    def show_password(self, state):
        if (QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked):
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.lineEdit_repeat_the_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.lineEdit_repeat_the_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def registration(self):
        cursor.execute(f"SELECT * FROM user WHERE login = '{self.lineEdit_login.text()}' and email = '{self.lineEdit_email.text()}'")
        print('1')
        data = cursor.fetchall()
        print('2')

        if data == [] and self.lineEdit_login.text() != "" and self.lineEdit_email.text() != "" and \
                (self.lineEdit_repeat_the_password.text() == self.lineEdit_password.text() and \
                (self.lineEdit_repeat_the_password.text() != '' and self.lineEdit_password.text() != '')) and \
                (self.lineEdit_email.text().count('@') == 1 and self.lineEdit_email.text()[0] != '@' and self.lineEdit_email.text().count('.') > 0 and \
                self.lineEdit_email.text().rfind('.') > self.lineEdit_email.text().rfind('@')):
            cursor.execute("INSERT INTO User (login, email, password) VALUES (?, ?, ?)", (self.lineEdit_login.text(), self.lineEdit_email.text(), self.lineEdit_password.text()))
            db.commit()
            print("Запись создана")
            error = QMessageBox()
            error.setIcon(QMessageBox.Icon.Information)
            error.setText('Запись создана')
            error.exec()
        elif data == [] and self.lineEdit_login.text() != "" and self.lineEdit_email.text() != "" and (self.lineEdit_repeat_the_password.text() != self.lineEdit_password.text()):
            print("Пароли не совпадают!")
            error = QMessageBox()
            error.setIcon(QMessageBox.Icon.Information)
            error.setText('Пароли не совпадают!!')
            error.exec()
        else:
            print("Такая запись уже имеется!")
            error = QMessageBox()
            error.setIcon(QMessageBox.Icon.Information)
            error.setText('Такая запись уже имеется!')
            error.exec()

    def openDialog2(self, event):
        Win_sign_in().openDialog3()
        self.hide()

class Win_Python_Chat(QMainWindow, Python_Chat):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_send.clicked.connect(lambda: self.message(self.label_login_name.text(), self.textEdit_input_message.toPlainText()))

    def message(self, name, message):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(current_datetime)
        # print(name + current_datetime)
        self.textBrowser_output_message.append(name + ' в ' + current_datetime)
        self.textBrowser_output_message.append(message)
        self.textBrowser_output_message.append('')
        self.textBrowser_output_message.repaint()
        self.textEdit_input_message.setText('')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Win_sign_in()

    window.show()
    sys.exit(app.exec())