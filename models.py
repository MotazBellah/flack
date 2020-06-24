from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

class Room(db.Model):
    """ Room model """

    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            }


class Message(db.Model):
    """ Message model """

    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship(Room)

    @property
    def serialize(self):
        return {
            'text': self.text,
            'time': self.time,
            }
