import sqlite3, hashlib, smtplib, ssl, os, time

from flask import Flask, request, g, jsonify
from random import*
from email.message import EmailMessage
from werkzeug.utils import secure_filename

app = Flask(__name__)
salt = os.getenv('SALT')
messages = []
message_id_counter = 0 # Лічильник повідомлень

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('handler/Python Chat.db')
    return db


def sha512(salt, data):
    sha512_salt = hashlib.sha512(salt.encode() + data.encode()).hexdigest()
    return sha512_salt


@app.route('/login', methods=['POST'])
def sign_in():
    """
    :input: {'login': str, 'password': str}
    :return: {'state': str, 'name': str} or {'state': str}
    """
    print(request.json)
    login = request.json['login']
    password = request.json['password']

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        f"SELECT * FROM user WHERE login = '{login}' or email = '{login}'"
    )
    data = cursor.fetchall()
    print(data)

    if login != '' and password != '':
        if data != []:
            if (login == data[0][1] or login == data[0][2]) and sha512(salt, password) == data[0][3]:
                name = data[0][1]
                return {'state': 'OK', 'name': name}
            elif (login == data[0][1] or login == data[0][2]) and sha512(salt, password) != data[0][3]:
                return {'state': 'NO'}
        else:
            return {'state': 'NO FOUND'}
    else:
        return {'state': 'EMPTY FIELDS'}


@app.route('/registration', methods=['POST'])
def registration():
    """
    :input: {'login': str, 'email': str, 'password': str, 'repeat_password': str}
    :return: state: str
    """
    print(request.json)
    login = request.json['login']
    email = request.json['email']
    password = request.json['password']
    repeat_password = request.json['repeat_password']

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        f"SELECT * FROM user WHERE login = '{login}' or email = '{email}'"
    )
    data = cursor.fetchall()
    print(data)

    if login != '' and email != '' and password != '' and repeat_password != '':
        if email.count('@') == 1 and email[0] != '@' and email.count('.') > 0 and email.rfind('.') > email.rfind('@'):
            if data == []:
                if repeat_password == password:
                    psw_sha512 = sha512(salt, password)
                    cursor.execute(
                        'INSERT INTO User (login, email, password, password_recovery_code) VALUES (?, ?, ?, ?)',
                        (login, email, psw_sha512, generation_code(cursor, email))
                    )
                    db.commit()
                    return 'OK'
                else:
                    return 'PASSWORDS DON`T MATCH!'
            else:
                return 'SUCH A RECORD ALREADY EXISTS!'
        else:
            return 'INCORRECT EMAIL ENTRY'
    else:
        return 'EMPTY FIELDS'


def send_email(email, message):
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


def generation_code(cursor, email):
    symvols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    code1 = []
    code2 = ''
    for _ in range(10):
        code1 += (sample(symvols, 1))

    for _ in code1:
        code2 += _

    print(code2)

    psw_rc_sha512 = sha512(salt, code2)

    cursor.execute(
        f'SELECT password_recovery_code FROM user'
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

    send_email(email, code2)

    return psw_rc_sha512


@app.route('/restoring_access_to_the_account', methods=['POST'])
def change_password():
    """
    :input: {'email': str, 'new_password': str, 'repeat_the_new_password': str, 'code_to_change_your_password': str}
    :return: state: str
    """
    print(request.json)
    email = request.json['email']
    new_password = request.json['new_password']
    repeat_the_new_password = request.json['repeat_the_new_password']
    code_to_change_your_password = request.json['code_to_change_your_password']

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        f"SELECT * FROM user WHERE email = '{email}'"
    )
    data = cursor.fetchall()
    print(data)

    if email != '' and new_password != '' and repeat_the_new_password != '' and code_to_change_your_password != '':
        if email.count('@') == 1 and email[0] != '@' and email.count('.') > 0 and email.rfind('.') > email.rfind('@'):
            if data != []:
                if new_password == repeat_the_new_password:
                    code_to_change_your_password = sha512(salt, code_to_change_your_password)
                    if code_to_change_your_password == data[0][4]:
                        new_password = sha512(salt, new_password)
                        cursor.execute(
                            f'UPDATE User SET password = ? WHERE password = ?', (new_password, data[0][3])
                        )
                        db.commit()
                        return 'OK'
                    else:
                        return 'INCORRECT RECOVERY CODE!'
                else:
                    return 'PASSWORDS DON`T MATCH!'
            else:
                return 'SUCH RECORD DOES NOT EXIST!'
        else:
            return 'INCORRECT EMAIL ENTRY'
    else:
        return 'EMPTY FIELDS'


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'OK': False, 'error': 'No file part'}
    file = request.files['file']
    if file.filename == '':
        return {'OK': False, 'error': 'No selected file'}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Додаємо повідомлення з файлом до загального списку
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        if file_extension in {'png', 'jpg', 'jpeg'}:
            file_type = 'IMAGE'
        elif file_extension in {'mp4', 'avi', 'mov'}:
            file_type = 'VIDEO'
        else:
            return {'OK': False, 'error': 'Invalid file type'}

        global message_id_counter
        messages.append(
            {'id': message_id_counter, 'login': request.form['login'], 'time': time.time(), 'text': f'[{file_type}]{UPLOAD_FOLDER}{filename}',
             'is_own_message': request.form['is_own_message'] == 'true'})
        message_id_counter += 1

        return {'OK': True, 'filename': filename}
    return {'OK': False, 'error': 'Invalid file type'}


@app.route('/send', methods=['POST'])
def send_view():
    """
    Відправити всім повідомлення.
    :input: {'login': str, 'text': str, 'is_own_message': bool}
    :return: {'OK': bool}
    """
    print(request.json)
    global message_id_counter
    login = request.json['login']
    text = request.json['text']
    is_own_message = request.json.get('is_own_message', False)

    messages.append({'id': message_id_counter, 'login': login, 'time': time.time(), 'text': text, 'is_own_message': is_own_message})
    message_id_counter += 1
    return {'OK': True}


@app.route('/edit_message', methods=['POST'])
def edit_message():
    data = request.json
    message_id = data.get('message_id')
    print(message_id)
    new_text = data.get('new_text')
    print(new_text)
    edited_time = data.get('edited_time')

    print(f"Редагування повідомлення з id: {message_id} на текст: {new_text}")  # Логування
    print(f"Поточний масив повідомлень: {messages}")

    if message_id is not None and new_text:
        for message in messages:
            print("messages", messages)
            if message['id'] == message_id:
                message['text'] = new_text
                message['edited_time'] = edited_time
                print(f"Повідомлення з id: {message_id} успішно відредаговано")
                return {'OK': True}
    print(f"Неправильний message_id або new_text")  # Логування
    return {'OK': False}


@app.route('/delete_message', methods=['POST'])
def delete_message():
    data = request.json
    message_id = data.get('message_id')

    print(f"Видалення повідомлення з id: {message_id}")  # Логування
    print(f"Поточний масив повідомлень: {messages}")

    if message_id is not None:
        for i, message in enumerate(messages):
            if message['id'] == message_id:
                del messages[i]
                print(f"Повідомлення з id: {message_id} успішно видалено")
                return {'OK': True}
    print(f"Неправильний message_id")  # Логування
    return {'OK': False}


@app.route('/messages', methods=['GET'])
def get_messages():
    after = float(request.args.get('after', 0))
    new_messages = [message for message in messages if message['time'] > after]
    return jsonify({'messages': new_messages})


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
