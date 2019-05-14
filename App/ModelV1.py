from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


import datetime


db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'Users'
    idPerson      = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(50), unique=True)
    email         = db.Column(db.String(40))
    name          = db.Column(db.String(50))
    lastName      = db.Column(db.String(50))
    position      = db.Column(db.String(50))
    password      = db.Column(db.String(255))
    status        = db.Column(db.Integer)
    signature     = db.Column(db.String(50), default = "llave")

    def __init__(self, username,email,name,lastName,position,password):
        self.username = username
        self.email = email
        self.name = name
        self.lastName = lastName
        self.position = position
        self.password = password
        self.status = status

    def __createPassword(sel, password):
        return generate_password_hash(password)

    def verifyPassword(self, password):
        return check_password_hash(self.password, password)

class Memo(db.Model):
    __tablename__ = 'Memo'
    idMemo        = db.Column(db.Integer, primary_key = True)
    title         = db.Column(db.String(50))
    memo_type     = db.Column(db.String(50))
    idPerson      = db.Column(db.Integer, ForeignKey("Users.idPerson"),nullable = False)
    content       = db.Column(db.String(50))
    
    def __init__(self,title, memo_type,idPerson,content):
        self.title = title
        self.memo_type = memo_type
        self.idPerson = idPerson
        self.content = content

class Bill(db.Model):
    __tablename__ = 'Bill'
    idBill        = db.Column(db.Integer, primary_key = True)
    title         = db.Column(db.String(50))
    content       = db.Column(db.String(50))
    
    def __init__(self, title,content):
        self.title = title
        self.content = content

class Rel_Bill_User(db.Model):
    __tablename__ = 'Rel_Bill_User'
    idRelBillUser = db.Column(db.Integer, primary_key = True)
    idPerson      = db.Column(db.Integer, ForeignKey("Users.idPerson"),nullable = False)
    idBill        = db.Column(db.Integer, ForeignKey("Bill.idBill"),nullable = False)
    
    def __init__(self, idPerson,idBill):
        self.idPerson = idPerson
        self.idBill = idBill

class Rel_Memo_User(db.Model):
    __tablename__ = 'Rel_Memo_User'
    idRelMemoUser = db.Column(db.Integer, primary_key = True)
    idPerson      = db.Column(db.Integer, ForeignKey("Users.idPerson"),nullable = False)
    idMemo        = db.Column(db.Integer, ForeignKey("Memo.idMemo"),nullable = False)
    
    def __init__(self, idPerson,idMemo):
        self.idPerson = idPerson
        self.idMemo = idMemo