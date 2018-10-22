import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    user_type = db.Column(db.String(100))
    password = db.Column(db.String(100))
    register_date = db.Column(db.String(100))
    last_login_date = db.Column(db.String(100))

    def __init__(self, name, surname, username, password):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.register_date = datetime.datetime.now()
        self.last_login_date = datetime.datetime.now()

