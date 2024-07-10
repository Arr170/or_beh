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


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    points = db.relationship('Point', backref='track', lazy=True)

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'points': [point.to_dict() for point in self.points]
            
            
        }

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'track_id': self.track_id
        }
    