from flask_sqlalchemy import SQLAlchemy
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
    password      = db.Column(db.String(66))
    signature     = db.Column(db.String(50))
    created_date  = db.Column(db.DateTime, default = datetime.datetime.now)
