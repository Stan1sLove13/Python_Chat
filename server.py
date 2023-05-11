import sqlite3, hashlib, smtplib, ssl, os, time

from flask import Flask, request, g
from random import*
from email.message import EmailMessage

app = Flask(__name__)
salt = os.getenv('SALT')
messages = []


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


@app.route('/messages')
def messages_view():
    """
    :input: ?after=float
    :return: [{'login': str, 'time': float, 'text': str}]
    """
    print(request.args)
    after = float(request.args['after'])

    filtered_messages = []
    for message in messages:
        if message['time'] > after:
            filtered_messages.append(message)

    return {'messages': filtered_messages}


@app.route('/send', methods=['POST'])
def send_view():
    """
    Відправити всім повідомлення.
    :input: {'login': str, 'text': str}
    :return: {'OK': bool}
    """
    print(request.json)
    login = request.json['login']
    text = request.json['text']

    messages.append({'login': login, 'time': time.time(), 'text': text})
    return {'OK': True}


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
