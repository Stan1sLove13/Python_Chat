import sqlite3
# import os
# import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///PythonChat.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
app.secret_key = 'qazwsxedcrfv1234'
# db.init_app(app)

# class User(db.Model):
#      id = db.Column(db.Integer, primary_key=True)
#      login = db.Column(db.String(20), unique=True, nullable=False)
#      email = db.Column(db.String(50), unique=True, nullable=False)
#      password = db.Column(db.String(100), nullable=False)
#
#      def __repr__(self):
#           return f"<Users {self.id}>"
#           # return '<User %r>' % self.id
#
# with app.app_context():
#      db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
     data = get_db()
     print(request)
     print(data[0])
     return data[0]
     # return str(data)
     # return "Hello"

def get_db():
     db = getattr(g, '_database', None)
     if db is None:
          db = g._database = sqlite3.connect('handler/Python Chat.db')
          cursor = db.cursor()
          cursor.execute("select login from User")
          all_data = cursor.fetchall()
          all_data = [str(val[0]) for val in all_data]
     return all_data
     # return cursor.fetchall()



if __name__ == '__main__':
     app.run(debug=True)