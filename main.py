import sys, ctypes, requests, threading


from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow
from sign_in import Ui_MainWindow as sign_in
from registration import Ui_MainWindow as registration
from Python_Chat import Ui_MainWindow as Python_Chat
from restoring_access_to_the_account import Ui_MainWindow as restoring_access_to_the_account
from datetime import datetime
from time import sleep


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

        self.pushButton_sign_in.clicked.connect(lambda: self.signIn(self.lineEdit_login.text(),
                                                                    self.lineEdit_password.text()))
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
        try:
            response = requests.post('http://127.0.0.1:5000/login', json={
                'login': login,
                'password': password
            })
            print(response.json()['state'])
            match response.json()['state']:
                case 'OK':
                    print('Успішний вхід')
                    openDialog('Information', 'Успішний вхід!', 'Успішний вхід!')
                    self.Python_Chat.show()
                    self.Python_Chat.label_login_name.setText(response.json()['name'])
                    self.hide()
                case 'NO':
                    print('Невірний пароль!')
                    openDialog('Information', 'Невірний пароль!', 'Невірний пароль!')
                case 'NO FOUND':
                    print('Не вдалося знайти акаунт!')
                    openDialog('Information', 'Не вдалося знайти акаунт!', 'Не вдалося знайти акаунт!')
                case 'EMPTY FIELDS':
                    print('Введіть логін та пароль!')
                    openDialog('Information', 'Введіть логін та пароль!', 'Введіть логін та пароль!')
        except requests.exceptions.ConnectionError:
            print('Вибачне. Наразі сервер не працює!')
            openDialog('Information', 'Вибачне. Наразі сервер не працює!', 'Вибачне. Наразі сервер не працює!')

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

        self.pushButton_registration.clicked.connect(lambda: self.registration(self.lineEdit_login.text(),
                                                                               self.lineEdit_email.text(),
                                                                               self.lineEdit_password.text(),
                                                                               self.lineEdit_repeat_the_password.text()))
        self.checkBox_show_password.stateChanged.connect(self.show_password)
        self.label_sign_in.mousePressEvent = self.showSignIn

    def show_password(self, state):
        if QtCore.Qt.CheckState(state) == QtCore.Qt.CheckState.Checked:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.lineEdit_repeat_the_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.lineEdit_repeat_the_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def registration(self, login, email, password, repeat_password):
        try:
            response = requests.post('http://127.0.0.1:5000/registration', json={
                'login': login,
                'email': email,
                'password': password,
                'repeat_password': repeat_password
            })
            print(response.text)
            match response.text:
                case 'OK':
                    print('Запис створено')
                    openDialog('Information', 'Запис створено', 'Запис створено')
                    Win_sign_in().showSignIn()
                    self.hide()
                case 'INCORRECT EMAIL ENTRY':
                    print('Неправильний запис пошти!')
                    openDialog('Information', 'Неправильний запис пошти!', 'Неправильний запис пошти!')
                case 'SUCH A RECORD ALREADY EXISTS!':
                    print('Такий запис вже є!')
                    openDialog('Information', 'Такий запис вже є!', 'Такий запис вже є!')
                case 'PASSWORDS DON`T MATCH!':
                    print('Паролі не співпадають!')
                    openDialog('Information', 'Паролі не співпадають!', 'Паролі не співпадають!')
                case 'EMPTY FIELDS':
                    print('Заповніть всі поля!')
                    openDialog('Information', 'Заповніть всі поля!', 'Заповніть всі поля!')
        except requests.exceptions.ConnectionError:
            print('Вибачне. Наразі сервер не працює!')
            openDialog('Information', 'Вибачне. Наразі сервер не працює!', 'Вибачне. Наразі сервер не працює!')

    def showSignIn(self, event):
        Win_sign_in().showSignIn()
        self.hide()


class Win_Python_Chat(QMainWindow, Python_Chat):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_send.clicked.connect(lambda: self.send(self.label_login_name.text(),
                                                               self.textEdit_input_message.toPlainText()))
        self.pushButton_logout.clicked.connect(self.logout)
        self.text_changed()
        self.textEdit_input_message.textChanged.connect(self.text_changed)
        threading.Thread(target=self.refresh).start()

    def text_changed(self):
        text = self.textEdit_input_message.toPlainText().strip()
        if text:
            self.pushButton_send.setEnabled(True)
        else:
            self.pushButton_send.setEnabled(False)

    def send(self, name, message):
        try:
            response = requests.post('http://127.0.0.1:5000/send', json={
                'login': name,
                'text': message
            })
            print(response.text)
            self.textEdit_input_message.setText('')
            self.textEdit_input_message.repaint()
        except requests.exceptions.ConnectionError:
            print('Вибачне. Наразі сервер не працює!')
            self.textBrowser_output_message.append('Вибачне. Наразі сервер не працює!')
            self.textBrowser_output_message.append('')
            self.textEdit_input_message.setText('')
            self.textEdit_input_message.repaint()

    def refresh(self):
        last_time = 0

        while True:
            try:
                response = requests.get('http://127.0.0.1:5000/messages',
                                        params={'after': last_time})
                print('Сервер працює!')
            except requests.exceptions.ConnectionError:
                print('Сервер не працює!')
                sleep(1)
                continue

            for message in response.json()['messages']:
                time_formated = datetime.fromtimestamp(message['time'])
                time_formated = time_formated.strftime('%Y-%m-%d %H:%M:%S')
                header = message['login'] + ' в ' + time_formated
                text = message['text']
                self.textBrowser_output_message.append(header)
                self.textBrowser_output_message.append(text)
                self.textBrowser_output_message.append('')
                last_time = message['time']

            sleep(1)

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
        self.pushButton_change_password.clicked.connect(
            lambda: self.change_password(self.lineEdit_email.text(),
                                         self.lineEdit_new_password.text(),
                                         self.lineEdit_repeat_the_new_password.text(),
                                         self.lineEdit_enter_the_code_to_change_your_password.text()))

    def change_password(self, email, new_password, repeat_the_new_password, code_to_change_your_password):
        try:
            response = requests.post('http://127.0.0.1:5000/restoring_access_to_the_account', json={
                'email': email,
                'new_password': new_password,
                'repeat_the_new_password': repeat_the_new_password,
                'code_to_change_your_password': code_to_change_your_password
            })
            print(response.text)
            match response.text:
                case 'OK':
                    print('Пароль змінено!')
                    openDialog('Information', 'Пароль змінено!', 'Пароль змінено!')
                    Win_sign_in().showSignIn()
                    self.hide()
                case 'INCORRECT EMAIL ENTRY':
                    print('Неправильний запис пошти!')
                    openDialog('Information', 'Неправильний запис пошти!', 'Неправильний запис пошти!')
                case 'SUCH RECORD DOES NOT EXIST!':
                    print('Не вдалося знайти аккаунт!')
                    openDialog('Information', 'Не вдалося знайти аккаунт!', 'Не вдалося знайти аккаунт!')
                case 'PASSWORDS DON`T MATCH!':
                    print('Паролі не співпадають!')
                    openDialog('Information', 'Паролі не співпадають!', 'Паролі не співпадають!')
                case 'INCORRECT RECOVERY CODE!':
                    print('Неправильний код відновлення!')
                    openDialog('Information', 'Неправильний код відновлення!', 'Неправильний код відновлення!')
                case 'EMPTY FIELDS':
                    print('Заповніть всі поля!')
                    openDialog('Information', 'Заповніть всі поля!', 'Заповніть всі поля!')
        except requests.exceptions.ConnectionError:
            print('Вибачне. Наразі сервер не працює!')
            openDialog('Information', 'Вибачне. Наразі сервер не працює!', 'Вибачне. Наразі сервер не працює!')

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
