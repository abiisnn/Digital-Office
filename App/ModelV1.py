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
    password      = db.Column(db.String(255))
    status        = db.Column(db.Integer, default = 0)
    position      = db.Column(db.String(50), default = "pendiente")
    signature     = db.Column(db.String(50), default = "llave")

    def __init__(self, username,email,name,lastName,password):
        self.username = username
        self.email = email
        self.name = name
        self.lastName = lastName
        self.password = generate_password_hash(password)

    def verifyPassword(self, password):
        return check_password_hash(self.password, password)

class Memo(db.Model):
    __tablename__ = 'Memo'
    idMemo        = db.Column(db.Integer, primary_key = True)
    title         = db.Column(db.String(50))
    memo_type     = db.Column(db.String(50))
    idPerson      = db.Column(db.Integer, db.ForeignKey("Users.idPerson"),nullable = False)
    content       = db.Column(db.String(50))

    def __init__(self,title, memo_type,idPerson,content):
        self.title = title
        self.memo_type = memo_type
        self.idPerson = idPerson
        self.content = content

class Bill(db.Model):
    __tablename__ = 'Bill'
    idBill        = db.Column(db.Integer, primary_key = True)
    idMeeting     = db.Column(db.Integer, db.ForeignKey("Meeting.idMeeting"),nullable = False)
    title         = db.Column(db.String(50))
    content       = db.Column(db.String(50))

    def __init__(self, title,content,idMeeting):
        self.idMeeting = idMeeting
        self.title = title
        self.content = content

class Meeting(db.Model):
    __tablename__ = 'Meeting'
    idMeeting     = db.Column(db.Integer, primary_key = True)
    idBill        = db.Column(db.Integer, db.ForeignKey("Bill.idBill"),nullable = False)

    def __init__(self, title,content,idBill):
        self.idBill = idBill
        self.title = title
        self.content = content

class Rel_Meeting_User(db.Model):
    __tablename__ = 'Rel_Meeting_User'
    idRelMeetingUser = db.Column(db.Integer, primary_key = True)
    idPerson         = db.Column(db.Integer, db.ForeignKey("Users.idPerson"),nullable = False)
    idMeeting        = db.Column(db.Integer, db.ForeignKey("Meeting.idMeeting"),nullable = False)

    def __init__(self, idPerson,idMeeting):
        self.idPerson = idPerson
        self.idMeeting = idMeeting

class Rel_Memo_User(db.Model):
    __tablename__ = 'Rel_Memo_User'
    idRelMemoUser = db.Column(db.Integer, primary_key = True)
    idPerson      = db.Column(db.Integer, db.ForeignKey("Users.idPerson"),nullable = False)
    idMemo        = db.Column(db.Integer, db.ForeignKey("Memo.idMemo"),nullable = False)

    def __init__(self, idPerson,idMemo):
        self.idPerson = idPerson
        self.idMemo = idMemo
