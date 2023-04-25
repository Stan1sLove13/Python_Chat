import sys, sqlite3, hashlib, smtplib, ssl, os, ctypes


from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow
from sign_in import Ui_MainWindow as sign_in
from registration import Ui_MainWindow as registration
from Python_Chat import Ui_MainWindow as Python_Chat
from restoring_access_to_the_account import Ui_MainWindow as restoring_access_to_the_account
from datetime import datetime
from random import*
from email.message import EmailMessage
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect('handler/Python Chat.db')
        return con
    except Error:
        print(Error)


salt = os.getenv('SALT')


def sha512(salt, data):
    sha512_salt = hashlib.sha512(salt.encode() + data.encode()).hexdigest()
    return sha512_salt


def openDialog(type, title, text):
    match type:
        case 'NoIcon':
            message = QMessageBox()
            message.setIcon(QMessageBox.Icon.NoIcon)
            message.setWindowTitle(title)
            message.setText(text)
            message.exec()
        case 'Question':
            message = QMessageBox()
            message.setIcon(QMessageBox.Icon.Question)
            message.setWindowTitle(title)
            message.setText(text)
            message.exec()
        case 'Information':
            message = QMessageBox()
            message.setIcon(QMessageBox.Icon.Information)
            message.setWindowTitle(title)
            message.setText(text)
            message.exec()
        case 'Warning':
            message = QMessageBox()
            message.setIcon(QMessageBox.Icon.Warning)
            message.setWindowTitle(title)
            message.setText(text)
            message.exec()
        case 'Critical':
            message = QMessageBox()
            message.setIcon(QMessageBox.Icon.Critical)
            message.setWindowTitle(title)
            message.setText(text)
            message.exec()


class Win_sign_in(QMainWindow, sign_in):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_sign_in.clicked.connect(lambda: self.signIn(self.lineEdit_login.text(), self.lineEdit_password.text()))
        self.label_registration.mousePressEvent = self.showRegistration
        self.label_forgot_password.mousePressEvent = self.showRestoringAccessToTheAccount
        self.checkBox_show_password.stateChanged.connect(self.show_password)

        self.Registration = Win_registration()
        self.Restoring_access_to_the_account = Win_restoring_access_to_the_account()
        self.Python_Chat = Win_Python_Chat()

    def show_password(self, state):
        if QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def signIn(self, login, password):
        if login != '' and password != '':
            db = sql_connection()
            cursor = db.cursor()
            cursor.execute(
                f"SELECT * FROM user WHERE login = '{login}' or email = '{login}'"
            )
            data = cursor.fetchall()
            password = sha512(salt, password)
            if data != [] and data[0][3] == password:
                print("Успішний вхід")
                openDialog('Information', 'Успішний вхід!', 'Успішний вхід!')
                self.Python_Chat.show()
                self.Python_Chat.label_login_name.setText(login)
                self.hide()
                db.close()
            elif data == []:
                print("Не вдалося знайти акаунт!")
                openDialog('Information', 'Не вдалося знайти акаунт!', 'Не вдалося знайти акаунт!')
            else:
                print("Невірні дані (Логін або пароль)!")
                openDialog('Information', 'Невірні дані (Логін або пароль)!', 'Невірні дані (Логін або пароль)!')
        else:
            print("Введіть логін та пароль!")
            openDialog('Information', 'Введіть логін та пароль!', 'Введіть логін та пароль!')

    def showRegistration(self, event):
        self.Registration.show()
        self.hide()

    def showSignIn(self):
        self.show()

    def showRestoringAccessToTheAccount(self, event):
        self.Restoring_access_to_the_account.show()
        self.hide()


class Win_registration(QMainWindow, registration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_registration.clicked.connect(self.registration)
        self.checkBox_show_password.stateChanged.connect(self.show_password)
        self.label_sign_in.mousePressEvent = self.showSignIn

    def send_email(self, email, message):
        sender = 'podlubnyi20023313@ukr.net'
        password = os.getenv('EMAIL_PASSWORD')

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

    def generation_code(self, cursor):
        symvols = '0123456789abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
        code1 = []
        code2 = ''
        for _ in range(10):
            code1 += (sample(symvols, 1))

        for _ in code1:
            code2 += _

        print(code2)

        psw_rc_sha512 = sha512(salt, code2)

        cursor.execute(
            f"SELECT password_recovery_code FROM user"
        )
        data = cursor.fetchall()

        while psw_rc_sha512 in data:
            code1 = []
            code2 = ''
            for _ in range(10):
                code1 += (sample(symvols, 1))
                print(code1)

            for _ in code1:
                print(code2)
                code2 += _

            print(code2)
            psw_rc_sha512 = sha512(salt, code2)

        print('psw_rc_SHA-512 with salt:', psw_rc_sha512)
        print('Хеш вверху!')

        self.send_email(self.lineEdit_email.text(), code2)

        return psw_rc_sha512

    def show_password(self, state):
        if QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.lineEdit_repeat_the_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.lineEdit_repeat_the_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def registration(self):
        if self.lineEdit_login.text() != '' and self.lineEdit_email.text() != '' and self.lineEdit_password.text() != '' and \
           self.lineEdit_repeat_the_password.text() != '':
            db = sql_connection()
            cursor = db.cursor()
            cursor.execute(
                f"SELECT * FROM user WHERE login = '{self.lineEdit_login.text()}' or email = '{self.lineEdit_email.text()}'"
            )
            data = cursor.fetchall()
            if data == [] and self.lineEdit_login.text() != "" and self.lineEdit_email.text() != "" and \
               (self.lineEdit_repeat_the_password.text() == self.lineEdit_password.text() and
               (self.lineEdit_repeat_the_password.text() != '' and self.lineEdit_password.text() != '')) and \
               (self.lineEdit_email.text().count('@') == 1 and self.lineEdit_email.text()[0] != '@' and
               self.lineEdit_email.text().count('.') > 0 and
               self.lineEdit_email.text().rfind('.') > self.lineEdit_email.text().rfind('@')):
                psw_sha512 = sha512(salt, self.lineEdit_password.text())
                print('psw_SHA-512 with salt:', psw_sha512)
                cursor.execute(
                    "INSERT INTO User (login, email, password, password_recovery_code) VALUES (?, ?, ?, ?)",
                    (self.lineEdit_login.text(), self.lineEdit_email.text(), psw_sha512, self.generation_code(cursor))
                )
                db.commit()
                print("Запис створено")
                openDialog('Information', 'Запис створено', 'Запис створено')
                Win_sign_in().showSignIn()
                self.hide()
                db.close()
            elif data == [] and self.lineEdit_login.text() != "" and self.lineEdit_email.text() != "" and \
                 self.lineEdit_repeat_the_password.text() != self.lineEdit_password.text():
                print("Паролі не співпадають!")
                openDialog('Information', 'Паролі не співпадають!', 'Паролі не співпадають!')
            else:
                print("Такий запис вже є!")
                openDialog('Information', 'Такий запис вже є!', 'Такий запис вже є!')
        else:
            print("Заповніть всі поля!")
            openDialog('Information', 'Заповніть всі поля!', 'Заповніть всі поля!')

    def showSignIn(self, event):
        Win_sign_in().showSignIn()
        self.hide()


class Win_Python_Chat(QMainWindow, Python_Chat):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_send.clicked.connect(lambda: self.message(self.label_login_name.text(), self.textEdit_input_message.toPlainText()))
        self.pushButton_logout.clicked.connect(self.logout)
        self.text_changed()
        self.textEdit_input_message.textChanged.connect(self.text_changed)

    def text_changed(self):
        text = self.textEdit_input_message.toPlainText().strip()
        if text:
            self.pushButton_send.setEnabled(True)
        else:
            self.pushButton_send.setEnabled(False)

    def message(self, name, message):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.textBrowser_output_message.append(name + ' в ' + current_datetime)
        self.textBrowser_output_message.append(message)
        self.textBrowser_output_message.append('')
        self.textBrowser_output_message.repaint()
        self.textEdit_input_message.setText('')

    def logout(self):
        Win_sign_in().showSignIn()
        self.hide()


class Win_restoring_access_to_the_account(QMainWindow, restoring_access_to_the_account):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label_sign_in.mousePressEvent = self.showSignIn
        self.checkBox_show_password.stateChanged.connect(self.show_password)
        self.checkBox_show_code.stateChanged.connect(self.show_code)
        self.pushButton_change_password.clicked.connect(self.change_password)

    def change_password(self):
        if self.lineEdit_email.text() != '' and self.lineEdit_new_password.text() != '' and \
           self.lineEdit_repeat_the_new_password.text() != '' and self.lineEdit_enter_the_code_to_change_your_password.text() != '':
            if self.lineEdit_email.text().count('@') == 1 and self.lineEdit_email.text()[0] != '@' and \
               self.lineEdit_email.text().count('.') > 0 and \
               self.lineEdit_email.text().rfind('.') > self.lineEdit_email.text().rfind('@'):
                db = sql_connection()
                cursor = db.cursor()
                cursor.execute(
                    f"SELECT * FROM user WHERE email = '{self.lineEdit_email.text()}'"
                )
                data = cursor.fetchall()
                if data != []:
                    if self.lineEdit_new_password.text() == self.lineEdit_repeat_the_new_password.text():
                        code_to_change_password = sha512(salt, self.lineEdit_enter_the_code_to_change_your_password.text())
                        if code_to_change_password == data[0][4]:
                            password = sha512(salt, self.lineEdit_new_password.text())
                            cursor.execute(
                                f"UPDATE User SET password = ? WHERE password = ?", (password, data[0][3])
                            )
                            db.commit()
                            print("Пароль змінено!")
                            openDialog('Information', 'Пароль змінено!', 'Пароль змінено!')
                            Win_sign_in().showSignIn()
                            self.hide()
                            db.close()
                        else:
                            print("Неправильний код відновлення!")
                            openDialog('Information', 'Неправильний код відновлення!', 'Неправильний код відновлення!')
                    else:
                        print("Паролі не співпадають!")
                        openDialog('Information', 'Паролі не співпадають!', 'Паролі не співпадають!')
                else:
                    print("Не вдалося знайти аккаунт!")
                    openDialog('Information', 'Не вдалося знайти аккаунт!', 'Не вдалося знайти аккаунт!')
            else:
                print("Некоректна пошта!")
                openDialog('Information', 'Некоректна пошта!', 'Некоректна пошта!')
        else:
            print("Заповніть всі поля!")
            openDialog('Information', 'Заповніть всі поля!', 'Заповніть всі поля!')

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

    def showSignIn(self, event):
        Win_sign_in().showSignIn()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('chat.ico'))
    window = Win_sign_in()

    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window.show()
    sys.exit(app.exec())
