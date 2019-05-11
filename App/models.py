from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    idPerson      = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(50), unique=True)
    email         = db.Column(db.String(40))
    name          = db.Column(db.String(50))
    lastName      = db.Column(db.String(50))
    employment    = db.Column(db.String(50))
    office        = db.Column(db.String(50))
    password      = db.Column(db.String(150))
    signature     = db.Column(db.String(50), default = "llave")
    created_date  = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, username,email,name,lastName,employment,office,password):
        self.username = username
        self.email = email
        self.name = name
        self.lastName = lastName
        self.employment = employment
        self.office = office
        self.password = self.__createPassword(password)

    def __createPassword(sel, password):
        return generate_password_hash(password)
