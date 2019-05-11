from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    idPerson      = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(50), unique=True)
    lastName      = db.Column(db.String(50), unique=True)
    email         = db.Column(db.String(40))
    password      = db.Column(db.String(66))
    employment    = db.Column(db.String(50), unique=True)
    signature     = db.Column(db.String(50), unique=True)
    office        = db.Column(db.String(50), unique=True)
    created_date  = db.Column(db.DateTime, default = datetime.datetime.now)
