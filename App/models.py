from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


import datetime


db = SQLAlchemy()

class UserRequest(db.Model):
    __tablename__ = 'UsersRequests'
    idPerson      = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(50), unique=True)
    email         = db.Column(db.String(40))
    name          = db.Column(db.String(50))
    lastName      = db.Column(db.String(50))
    password      = db.Column(db.String(255))
    created_date  = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, username,email,name,lastName,password):
        self.username = username
        self.email = email
        self.name = name
        self.lastName = lastName
        self.password = self.__createPassword(password)

    def __createPassword(sel, password):
        return generate_password_hash(password)

    def verifyPassword(self, password):
        return check_password_hash(self.password, password)

class User(db.Model):
    __tablename__ = 'Users'
    idPerson      = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(50), unique=True)
    email         = db.Column(db.String(40))
    name          = db.Column(db.String(50))
    lastName      = db.Column(db.String(50))
    employment    = db.Column(db.String(50))
    password      = db.Column(db.String(255))
    signature     = db.Column(db.String(50), default = "llave")

    def __init__(self, username,email,name,lastName,employment,password):
        self.username = username
        self.email = email
        self.name = name
        self.lastName = lastName
        self.employment = employment
        self.password = password

    def __createPassword(sel, password):
        return generate_password_hash(password)

    def verifyPassword(self, password):
        return check_password_hash(self.password, password)
