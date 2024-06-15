from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    time = db.Column(db.Integer)
    track = db.Column(db.String(1))
    date = db.Column(db.String(10))\
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time, 
            'track': self.track, 
            'date': self.date
        }



    