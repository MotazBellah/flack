from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# from datetime import datetime, timezone
import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Room(db.Model):
    """ Room model """

    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)


class Message(db.Model):
    """ Message model """

    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    room = db.relationship(Room)
    # time = db.Column(db.String(250), default=datetime.now(timezone.utc).astimezone().strftime("%a, %d %b %Y %H:%M:%S"))
