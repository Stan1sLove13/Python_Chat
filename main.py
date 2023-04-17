import sys, sqlite3, hashlib, smtplib, ssl, os

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow
from sign_in import Ui_MainWindow as sign_in
from registration import Ui_MainWindow as registration
from Python_Chat import Ui_MainWindow as Python_Chat
from restoring_access_to_the_account import Ui_MainWindow as restoring_access_to_the_account
from datetime import datetime
from random import*
from email.message import EmailMessage

db = sqlite3.connect('handler/Python Chat.db')
cursor = db.cursor()

class Win_sign_in(QMainWindow, sign_in):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_sign_in.clicked.connect(lambda: self.openDialog1(self.lineEdit_login.text(), self.lineEdit_password.text()))
        self.label_registration.mousePressEvent = self.openDialog2
        self.label_forgot_password.mousePressEvent = self.openDialog4
        self.checkBox_show_password.stateChanged.connect(self.show_password)

        self.Registration = Win_registration()
        self.Restoring_access_to_the_account = Win_restoring_access_to_the_account()
        self.Python_Chat = Win_Python_Chat()

    def show_password(self, state):
        if (QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked):
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def openDialog1(self, login, password):
        cursor.execute(f"SELECT * FROM user WHERE login = '{login}' or email = '{login}'")
        data = cursor.fetchall()

        salt = 'hyi'
        password = hashlib.sha512(salt.encode() + password.encode()).hexdigest()

        # if data != [] and data[0][3] == password and login != []
        if data != [] and data[0][3] == password:
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

    def openDialog4(self, event):
        self.Restoring_access_to_the_account.show()
        self.hide()

class Win_registration(QMainWindow, registration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_registration.clicked.connect(self.registration)
        self.checkBox_show_password.stateChanged.connect(self.show_password)
        self.label_sign_in.mousePressEvent = self.openDialog2

    def send_email(self, email, message):
        print('aaaaa!!!!!')
        sender = 'podlubnyi20023313@ukr.net'
        password = os.getenv('EMAIL_PASSWORD')
        print(password)
        print(email)
        print(type(email))
        print(message)

        subject = 'Код для відновлення аккаунту!'
        body = f'Код для відновлення: {message}\n' \
               f'Нікому його не передавайте!'

        em = EmailMessage()
        em['From'] = sender
        em['To'] = email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.ukr.net', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, email, em.as_string())

        # server = smtplib.SMTP_SSL('smtp.ukr.net', 465, context=context)
        # server.starttls()
        # server.login(sender, password)
        # server.sendmail(sender, email, message)

        # try:
        #     server.login(sender, password)
        #     server.sendmail(sender, email, f'Subject: Код для відновлення аккаунту!\n{message}')
        #
        #     return 'The message was sent successfully!'
        #     print('1')
        # except Exception as _ex:
        #     return f'{_ex}\nCheck your login or password please!'
        #     print('2')

    def generation_code(self):
        symvols = '0123456789abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
        # print(symvols)
        # code = (sample(symvols, 10))
        # print(code)
        code1 = []
        code2 = ''
        # for _ in range(10):
        #     code += sample(symvols)
        #     print(code)
        # code = cede.text()
        # print(code)
        # return code
        for _ in range(10):
            code1 += (sample(symvols, 1))
            print(code1)

        for _ in code1:
            print(code2)
            code2 += _

        print(code2)
        print(type(self.lineEdit_login.text()))
        print(type(code2))

        salt = 'hyi'
        psw_rc_sha512 = hashlib.sha512(salt.encode() + code2.encode())
        print(psw_rc_sha512)
        print('psw_rc_SHA-512 with salt:', psw_rc_sha512.hexdigest())
        print('Хеш вверху!')

        self.send_email(self.lineEdit_email.text(), code2)

        return psw_rc_sha512.hexdigest()

    def show_password(self, state):
        if QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.lineEdit_repeat_the_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.lineEdit_repeat_the_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def registration(self):
        # cursor.execute(f"SELECT * FROM user WHERE login = '{self.lineEdit_login.text()}' and email = '{self.lineEdit_email.text()}'")
        cursor.execute(f"SELECT * FROM user WHERE login = '{self.lineEdit_login.text()}' or email = '{self.lineEdit_email.text()}'")
        print('1')
        data = cursor.fetchall()
        print(data)
        # print(data[0][3].encode())
        print('2')

        # a = self.generation_code()
        # print(a)

        if data == [] and self.lineEdit_login.text() != "" and self.lineEdit_email.text() != "" and \
                (self.lineEdit_repeat_the_password.text() == self.lineEdit_password.text() and \
                (self.lineEdit_repeat_the_password.text() != '' and self.lineEdit_password.text() != '')) and \
                (self.lineEdit_email.text().count('@') == 1 and self.lineEdit_email.text()[0] != '@' and self.lineEdit_email.text().count('.') > 0 and \
                self.lineEdit_email.text().rfind('.') > self.lineEdit_email.text().rfind('@')):

            salt = 'hyi'
            psw_sha512 = hashlib.sha512(salt.encode() + self.lineEdit_password.text().encode())
            print('psw_SHA-512 with salt:', psw_sha512.hexdigest())
            # dsadw @ gmail.com
            # cursor.execute("INSERT INTO User (login, email, password, password_recovery_code) VALUES (?, ?, ?, ?)", (self.lineEdit_login.text(), self.lineEdit_email.text(), self.lineEdit_password.text(), self.generation_code()))
            cursor.execute("INSERT INTO User (login, email, password, password_recovery_code) VALUES (?, ?, ?, ?)", (self.lineEdit_login.text(), self.lineEdit_email.text(), psw_sha512.hexdigest(), self.generation_code()))
            db.commit()

            # self.send_email(self.lineEdit_email.text(),self.lineEdit_password)

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

        # if self.textEdit_input_message.toPlainText() == '':
        #     self.pushButton_send.setEnabled(False)
        # else:
        #     self.pushButton_send.setEnabled(True)

        # self.textEdit_input_message.textChanged.connect(lambda text: self.pushButton_send.setEnabled(bool(text)))

        # self.textEdit_input_message.textChanged.connect(lambda: self.changeButton(self.textEdit_input_message.toPlainText()))

        self.pushButton_send.clicked.connect(lambda: self.message(self.label_login_name.text(), self.textEdit_input_message.toPlainText()))
        self.text_changed()
        self.textEdit_input_message.textChanged.connect(self.text_changed)

    def text_changed(self):
        text = self.textEdit_input_message.toPlainText().strip()
        if text:
            self.pushButton_send.setEnabled(True)
        else:
            self.pushButton_send.setEnabled(False)

    # def changeButton(self, value):
    #     if value == '':
    #         self.ushButton_send.setEnabled(False)
    #     else:
    #         self.ushButton_send.setEnabled(True)

    def message(self, name, message):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(current_datetime)
        # print(name + current_datetime)
        self.textBrowser_output_message.append(name + ' в ' + current_datetime)
        self.textBrowser_output_message.append(message)
        self.textBrowser_output_message.append('')
        self.textBrowser_output_message.repaint()
        self.textEdit_input_message.setText('')

class Win_restoring_access_to_the_account(QMainWindow, restoring_access_to_the_account):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label_sign_in.mousePressEvent = self.openDialog2
        self.checkBox_show_password.stateChanged.connect(self.show_password)
        self.checkBox_show_code.stateChanged.connect(self.show_code)
        self.pushButton_change_password.clicked.connect(self.change_password)

    def change_password(self):
        cursor.execute(f"SELECT * FROM user WHERE email = '{self.lineEdit_email.text()}'")
        print('1')
        data = cursor.fetchall()
        print('2')
        print(data)
        print(data[0][3])
        print(type(data))
        print('2', data[0][3])
        print(type(data[0][3]))

        # print(data[0][3].encode())
        # print(b't')
        # md5 = hashlib.sha512(b't')
        # print('SHA-512:', md5.hexdigest())

        # a = self.generation_code()
        # print(a)

        salt = 'hyi'
        password = hashlib.sha512(salt.encode() + self.lineEdit_new_password.text().encode())
        code_to_change_password = hashlib.sha512(salt.encode() + self.lineEdit_enter_the_code_to_change_your_password.text().encode())


        if data != [] and self.lineEdit_email.text() != "" and \
                (self.lineEdit_repeat_the_new_password.text() == self.lineEdit_new_password.text() and \
                (self.lineEdit_repeat_the_new_password.text() != '' and self.lineEdit_new_password.text() != '')) and \
                (self.lineEdit_email.text().count('@') == 1 and self.lineEdit_email.text()[0] != '@' and self.lineEdit_email.text().count('.') > 0 and \
                self.lineEdit_email.text().rfind('.') > self.lineEdit_email.text().rfind('@')):

            # cursor.execute(f"UPDATE User SET password = {self.lineEdit_new_password.text()} WHERE password = {data[0][3]}", (self.lineEdit_new_password.text()))
            print(type(self.lineEdit_new_password.text()))
            # cursor.execute(f"UPDATE User SET password = {self.lineEdit_new_password.text()} WHERE password = {self.data[0][3]}")

            # cursor.execute(f"UPDATE User SET password = '{self.lineEdit_new_password.text()}' WHERE password = '{data[0][3]}'")
            # if self.lineEdit_enter_the_code_to_change_your_password.text() == data[0][4]:
            if code_to_change_password.hexdigest() == data[0][4]:
                # cursor.execute(f"UPDATE User SET password = ? WHERE password = ?", (self.lineEdit_new_password.text(), data[0][3]))
                cursor.execute(f"UPDATE User SET password = ? WHERE password = ?", (password.hexdigest(), data[0][3]))
            # cursor.execute(f"UPDATE User SET password = '2' WHERE password = 'q'")
                db.commit()
                print("Запись создана")
                error = QMessageBox()
                error.setIcon(QMessageBox.Icon.Information)
                error.setText('Запись создана')
                error.exec()
            else:
                print("Не верный код для востаговления!")
                print(code_to_change_password.hexdigest())
                error = QMessageBox()
                error.setIcon(QMessageBox.Icon.Information)
                error.setText('Не верный код для востаговления!')
                error.exec()
        # elif data == [] and self.lineEdit_login.text() != "" and self.lineEdit_email.text() != "" and (self.lineEdit_repeat_the_password.text() != self.lineEdit_password.text()):
        #     print("Пароли не совпадают!")
        #     error = QMessageBox()
        #     error.setIcon(QMessageBox.Icon.Information)
        #     error.setText('Пароли не совпадают!!')
        #     error.exec()
        else:
            print("Такая запись не существует!")
            error = QMessageBox()
            error.setIcon(QMessageBox.Icon.Information)
            error.setText('Такая запись не существует!')
            error.exec()

    def show_password(self, state):
        if QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked:
            self.lineEdit_new_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.lineEdit_repeat_the_new_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_new_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.lineEdit_repeat_the_new_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def show_code(self, state):
        if QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked:
            self.lineEdit_enter_the_code_to_change_your_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_enter_the_code_to_change_your_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def openDialog2(self, event):
        Win_sign_in().openDialog3()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Win_sign_in()

    window.show()
    sys.exit(app.exec())
