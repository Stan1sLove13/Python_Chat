import os
import sys, ctypes, requests, threading

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QUrl, pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QComboBox, QPushButton, QFileDialog, QWidget,\
    QVBoxLayout, QLabel, QHBoxLayout, QListWidgetItem, QDialog, QDialogButtonBox, QSlider, QLineEdit
from GUI.sign_in import Ui_MainWindow as sign_in
from GUI.registration import Ui_MainWindow as registration
from GUI.Python_Chat import Ui_MainWindow as Python_Chat
from GUI.restoring_access_to_the_account import Ui_MainWindow as restoring_access_to_the_account
from datetime import datetime


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
                    self.close()
                    user_login = response.json()['name']
                    chat_window = Win_Python_Chat(user_login)
                    chat_window.showPythonChat(user_login)
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
        self.close()
        Win_registration().showRegistration()

    def showSignIn(self):
        self.show()

    def showRestoringAccessToTheAccount(self, event):
        self.close()
        Win_restoring_access_to_the_account().showRestoringAccessToTheAccount()


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
                    self.close()
                    Win_sign_in().showSignIn()
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
        self.close()
        Win_sign_in().showSignIn()

    def showRegistration(self):
        self.show()


class Win_Python_Chat(QMainWindow, Python_Chat):
    # Оголошення сигналу на рівні класу
    update_ui_signal = pyqtSignal(str, str, int) # параметри типу сигналу

    def __init__(self, user_login):
        super().__init__()
        self.setupUi(self)
        self.user_login = user_login

        self.last_time = 0

        self.pushButton_send.clicked.connect(
            lambda: self.send(self.user_login, self.textEdit_input_message.toPlainText()))
        self.pushButton_logout.clicked.connect(self.logout)
        self.text_changed()
        self.textEdit_input_message.textChanged.connect(self.text_changed)

        self.comboBox.addItems(['😊', '😂', '😍', '😎', '😭', '😡', '👍', '👎', '💖', '🎉'])
        self.comboBox.activated.connect(self.insert_emoji)

        self.thread1_state = True
        self.thread1 = threading.Thread(target=self.refresh)
        self.thread1.start()

        self.pushButton_send_file.clicked.connect(self.send_file)

        self.update_ui_signal.connect(self.update_ui)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(5000)

    def send_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                   "Images (*.png *.jpg *.jpeg);;Videos (*.mp4 *.avi *.mov)")
        if file_name:
            try:
                with open(file_name, 'rb') as f:
                    response = requests.post('http://127.0.0.1:5000/upload',
                                             data={'login': self.user_login, 'is_own_message': 'true'},
                                             files={'file': f})
                print(response.text)
                if not response.json().get('OK'):
                    self.add_list_item('Не вдалося відправити файл: ' + response.json().get('error', ''))
            except requests.exceptions.ConnectionError:
                print('Вибачте. Наразі сервер не працює!')
                self.add_list_item('Вибачте. Наразі сервер не працює!')

    def text_changed(self):
        text = self.textEdit_input_message.toPlainText().strip()
        self.pushButton_send.setEnabled(bool(text))

    def send(self, name, message):
        try:
            response = requests.post('http://127.0.0.1:5000/send', json={
                'login': name,
                'text': message,
                'is_own_message': name == self.user_login
            })
            print(response.text)
            self.textEdit_input_message.setText('')
            self.textEdit_input_message.repaint()
        except requests.exceptions.ConnectionError:
            print('Вибачте. Наразі сервер не працює!')
            self.add_list_item('Вибачте. Наразі сервер не працює!')
            self.textEdit_input_message.setText('')
            self.textEdit_input_message.repaint()

    def refresh(self):
        try:
            scroll_position = self.listWidget_output_message.verticalScrollBar().value()  # Зберігаємо поточне положення прокрутки
            response = requests.get('http://127.0.0.1:5000/messages', params={'after': 0})  # Отримуємо всі повідомлення
            if response.status_code == 200:
                messages = response.json()['messages']
                self.listWidget_output_message.clear()  # Очищаємо список перед оновленням
                for message in messages:
                    time_formated = datetime.fromtimestamp(message['time']).strftime('%Y-%m-%d %H:%M:%S')
                    if message['login'] == self.user_login:
                        header = f'Ви в {time_formated}'
                    else:
                        header = f'{message["login"]} в {time_formated}'

                    # Додаємо перевірку на наявність часу редагування
                    if 'edited_time' in message:
                        edited_time_formated = datetime.fromtimestamp(message['edited_time']).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        header += f" (редаговано: {edited_time_formated})"

                    self.update_ui_signal.emit(header, message['text'], message['id'])
                    self.last_time = max(self.last_time,
                                         message['time'])  # Оновлюємо останній час тільки для нових повідомлень
            self.listWidget_output_message.verticalScrollBar().setValue(
                scroll_position)  # Відновлюємо положення прокрутки
        except requests.ConnectionError:
            print("Сервер не доступний")
        except Exception as e:
            print(f"Error while refreshing messages: {e}")

    def update_ui(self, header, text, message_id):
        if text.startswith('[IMAGE]'):
            image_path = text.replace('[IMAGE]', '').strip()
            self.add_list_item(f"{header}\n{image_path}", message_id, html_text=image_path, is_html=True)
        elif text.startswith('[VIDEO]'):
            video_path = text.replace('[VIDEO]', '').strip()
            self.add_list_item(f"{header}\n{video_path}", message_id, html_text=video_path, is_html=True, is_video=True)
        else:
            combined_text = f"{header}\n{text}"
            self.add_list_item(combined_text, message_id)

    def add_list_item(self, text, message_id, html_text=None, is_html=False, is_video=False):
        # Перевіряємо чи повідомлення вже існує, щоб уникнути дублікатів
        for i in range(self.listWidget_output_message.count()):
            item = self.listWidget_output_message.item(i)
            container_widget = self.listWidget_output_message.itemWidget(item)
            if container_widget.message_id == message_id:
                text_label = container_widget.layout().itemAt(0).widget()
                text_label.setText(text)
                return

        # Якщо повідомлення не існує, додаємо його як нове
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_widget.message_id = message_id  # Зберігаємо message_id в контейнері

        if is_html and html_text:
            # Розділяємо header і text для заголовка
            header, actual_text = text.split('\n', 1)
            header_label = QLabel(header)
            header_label.setWordWrap(True)  # Додаємо перенесення рядків для заголовка
            header_label.setMaximumWidth(350)  # Обмежуємо ширину заголовка
            container_layout.addWidget(header_label)

            if not is_video:
                image_label = QLabel()
                image_label.setFixedSize(300, 300)  # Встановлюємо розміри для зображення
                if os.path.exists(html_text):
                    try:
                        pixmap = QPixmap(html_text)
                        scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio,
                                                      Qt.TransformationMode.SmoothTransformation)
                        image_label.setPixmap(scaled_pixmap)
                        image_label.setFixedSize(scaled_pixmap.size())  # Динамічно змінюємо розмір QLabel
                    except Exception as e:
                        print(e)
                        image_label.setText(f"Error loading image: {e}")
                else:
                    image_label.setText("Image not found")
                container_layout.addWidget(image_label)
            else:
                video_widget = QVideoWidget()
                video_widget.setMinimumSize(300, 300)
                video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
                video_player = QMediaPlayer(container_widget)
                audio_output = QAudioOutput(container_widget)
                video_player.setVideoOutput(video_widget)
                video_player.setAudioOutput(audio_output)
                video_player.setSource(QUrl.fromLocalFile(html_text))
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setRange(0, 100)
                slider.sliderMoved.connect(video_player.setPosition)
                video_player.positionChanged.connect(lambda position: slider.setValue(position))
                video_player.durationChanged.connect(lambda duration: slider.setRange(0, duration))
                control_layout = QHBoxLayout()
                play_button = QPushButton("Play")
                pause_button = QPushButton("Pause")
                stop_button = QPushButton("Stop")
                play_button.clicked.connect(lambda: self.play_video(video_player))
                pause_button.clicked.connect(lambda: self.pause_video(video_player))
                stop_button.clicked.connect(lambda: self.stop_video(video_player))
                control_layout.addWidget(play_button)
                control_layout.addWidget(pause_button)
                control_layout.addWidget(stop_button)
                container_layout.addWidget(video_widget)
                container_layout.addWidget(slider)
                container_layout.addLayout(control_layout)

            # Додаємо тільки кнопку видалення для зображень і відео
            if header.startswith('Ви в'):
                button_layout = QHBoxLayout()
                delete_button = QPushButton('Видалити')
                delete_button.clicked.connect(lambda: self.delete_message(container_widget, message_id))
                button_layout.addWidget(delete_button)
                container_layout.addLayout(button_layout)
        else:
            header, actual_text = text.split('\n', 1)
            header_label = QLabel(header)
            header_label.setWordWrap(True)  # Додаємо перенесення рядків для заголовка
            header_label.setMaximumWidth(350)  # Обмежуємо ширину заголовка

            actual_text = QLabel(actual_text)
            actual_text.setWordWrap(True)  # Додаємо перенесення рядків для тексту
            actual_text.setMaximumWidth(350)  # Обмежуємо ширину тексту

            container_layout.addWidget(header_label)
            container_layout.addWidget(actual_text)
            # Додаємо кнопки редагування та видалення для текстових повідомлень
            if header.startswith('Ви в'):
                button_layout = QHBoxLayout()
                edit_button = QPushButton('Редагувати')
                delete_button = QPushButton('Видалити')
                edit_button.clicked.connect(lambda: self.edit_message_dialog(container_widget, message_id))
                delete_button.clicked.connect(lambda: self.delete_message(container_widget, message_id))
                button_layout.addWidget(edit_button)
                button_layout.addWidget(delete_button)
                container_layout.addLayout(button_layout)

        list_item = QListWidgetItem()
        list_item.setSizeHint(container_widget.sizeHint())
        self.listWidget_output_message.addItem(list_item)
        self.listWidget_output_message.setItemWidget(list_item, container_widget)

    def play_video(self, video_player):
        self.timer.stop()
        video_player.play()
        video_player.mediaStatusChanged.connect(self.handle_video_status)

    def handle_video_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.timer.start(5000)  # Відновлення оновлення кожні 5 секунд

    def pause_video(self, video_player):
        video_player.pause()
        self.timer.start(5000)  # Відновлення оновлення кожні 5 секунд

    def stop_video(self, video_player):
        video_player.stop()
        self.timer.start(5000)  # Відновлення оновлення кожні 5 секунд

    def edit_message_dialog(self, container_widget, message_id):
        text_label_2 = container_widget.layout().itemAt(1).widget()

        current_text_2 = text_label_2.text()

        actual_text = current_text_2.split('\n', 1)[0]

        dialog = QDialog(self)
        dialog.setWindowTitle('Редагувати повідомлення')

        layout = QVBoxLayout(dialog)

        label = QLabel('Введіть новий текст:', dialog)
        layout.addWidget(label)

        text_input = QLineEdit(actual_text, dialog)
        layout.addWidget(text_input)

        comboBox = QComboBox(dialog)
        comboBox.addItems(['😊', '😂', '😍', '😎', '😭', '😡', '👍', '👎', '💖', '🎉'])
        layout.addWidget(comboBox)

        button_box = QDialogButtonBox(dialog)
        button_box.addButton("Так", QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton("Скасувати", QDialogButtonBox.ButtonRole.RejectRole)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        comboBox.activated.connect(lambda index: text_input.insert(comboBox.itemText(index)))

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_text = text_input.text()
            if new_text != actual_text:
                print('new_text', new_text)
                self.edit_message(new_text, message_id)
            else:
                print('new_text == actual', f"{new_text}, {actual_text}")
                return

    def edit_message(self, new_text, message_id):
        try:
            edited_time = datetime.now().timestamp()  # Отримуємо поточний час редагування як timestamp
            print("edited_time", edited_time)
            response = requests.post('http://127.0.0.1:5000/edit_message',
                                     json={'message_id': message_id, 'new_text': new_text, 'edited_time': edited_time})
        except Exception as e:
            print(f"Error while editing message: {e}")

    def delete_message(self, container_widget, message_id):
        response = requests.post('http://127.0.0.1:5000/delete_message', json={'message_id': message_id})
        if response.json().get('OK'):
            for i in range(self.listWidget_output_message.count()):
                item = self.listWidget_output_message.item(i)
                if self.listWidget_output_message.itemWidget(item) == container_widget:
                    self.listWidget_output_message.takeItem(i)
                    container_widget.deleteLater()
                    break

    def insert_emoji(self, index):
        emoji = self.comboBox.itemText(index)  # Отримуємо емодзі за індексом
        self.textEdit_input_message.insertPlainText(emoji)

    def logout(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle('Підтвердження виходу')
        msgBox.setText("Ви впевнені, що хочете вийти?")
        msgBox.setIcon(QMessageBox.Icon.Question)  # Встановлюємо іконку знака питання

        # Додаємо кнопки "Так" та "Ні"
        yes_button = msgBox.addButton("Так", QMessageBox.ButtonRole.YesRole)
        no_button = msgBox.addButton("Ні", QMessageBox.ButtonRole.NoRole)

        msgBox.setDefaultButton(no_button)
        msgBox.exec()

        # Перевіряємо, яку кнопку було натиснуто
        if msgBox.clickedButton() == yes_button:
            self.thread1_state = False
            self.thread1.join()
            print('Потік 1 завершився')
            self.close()
            Win_sign_in().showSignIn()
        else:
            pass

    def showPythonChat(self, name):
        self.show()
        self.label_login_name.setText(name)


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
                    self.close()
                    Win_sign_in().showSignIn()
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
        self.close()
        Win_sign_in().showSignIn()

    def showRestoringAccessToTheAccount(self):
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('image/chat.ico'))
    window = Win_sign_in()

    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window.show()
    sys.exit(app.exec())
